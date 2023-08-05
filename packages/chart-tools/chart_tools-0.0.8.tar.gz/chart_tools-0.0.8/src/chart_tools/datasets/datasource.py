from dataclasses import dataclass
from operator import countOf
import pandas as pd
import requests
import json
import os
from hashlib import md5


def hash_kwargs(**kwargs):
    text = str(kwargs)
    int_hash = int(md5(text.encode('utf-8')).hexdigest(), 16)
    return int(str(int_hash)[0:14])


def check_internet():
    try:
        request = requests.get("https://www.google.com/", timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout) as e:
        return False


@dataclass
class Source:
    __user: str
    __repo: str
    __branch: str
    __path: str
    __datasets = []
    truncated_datasets = False
    cache = {}

    # Getters - no logic
    @property
    def user(self):
        return self.__user
    @property
    def repo(self):
        return self.__repo
    @property
    def branch(self):
        return self.__branch
    @property
    def path(self):
        return self.__path

    # Getters - logic
    @property
    def datasets(self) -> list:
        if self.__datasets == []: # Only load file structure when needed
            self.__datasets = self.refresh_datasets()
        return self.__datasets

    @property
    def subdirs(self) -> list:
        """ First layer of sub-directories in datasource. """
        return list(set([
                f.split('/')[0] for f in self.datasets if "/" in f
            ]))

    @property
    def datasets_base(self) -> list:
        """ Base filenames, without path """
        return [f.rsplit('/', 1)[-1] for f in self.datasets]

    @property
    def root(self) -> str:
        """
        User-friendly url to visit the source on Github.com
        """
        return f"https://github.com/{self.user}/{self.repo}/tree/{self.branch}/{self.path}"
    
    @property
    def req_url(self) -> str:
        """
        Url to Github API for getting all files in repo and branch
        """
        return f"https://api.github.com/repos/{self.user}/{self.repo}/git/trees/{self.branch}?recursive=1"
    
    def get(self, dataset_name):
        return self.cache[dataset_name].copy()
    
    # Setters - include validation logic
    @user.setter
    def user(self, value):
        if "/" in value:
            raise ValueError("Github username can't have slashes")
        self.__user = value

    @repo.setter
    def repo(self, value):
        if "/" in value:
            raise ValueError("Github repository name can't have slashes")
        self.__repo = value

    @branch.setter
    def branch(self, value):
        if "/" in value:
            raise ValueError("Github branch name can't have slashes")
        self.__branch = value

    @path.setter
    def path(self, value):
        if value.endswith("/"):
            raise ValueError("Path must not end with a slash")
        self.__path = value
        # Update datasets since path changed
        self.refresh_datasets()


    def file_url(self, filename) -> str:
        """
        Url to raw, downloadable file
        """
        path = f"{self.path}/" if len(self.path) > 0 else self.path
        return f"https://raw.githubusercontent.com/{self.user}/{self.repo}/{self.branch}/{path}{filename}.csv"


    def req_files(self) -> list:
        """ Request files """
        if check_internet():
            return requests.get(self.req_url).json()
        return None
    

    def dir_contents(self, dir) -> list:
        """ Get filenames in directory """
        return [f.removeprefix(f"{dir}/") for f in self.datasets if f.startswith(dir)]


    def load(self, fname, save=True, **kwargs) -> pd.DataFrame:

        if fname in self.cache and save == False:
            self.cache.pop(fname)

        if fname in self.cache and save == True:
            # Return cached df ONLY if keyword arguments are the same
            if hash_kwargs(**kwargs) == self.cache[fname]['kwargs_hash']:
                return self.cache[fname]['df'].copy()

        if not check_internet():
            return pd.DataFrame()

        if self.datasets == []:
            return pd.DataFrame()
        
        if countOf(self.datasets, fname) == 1:
            df = pd.read_csv(self.file_url(fname), **kwargs)
            if save:
                # Save both the df, and the cache of the keyword arguments
                self.cache[fname] = {'df': df, 'kwargs_hash': hash_kwargs(**kwargs)}
            return df.copy()

        if countOf(self.datasets_base, fname) == 1:
            # Allows you to use base filename ONLY if there are no duplicates
            full_fname = [f for f in self.datasets if f.rsplit('/', 1)[-1] == fname][0]
            df = pd.read_csv(self.file_url(full_fname), **kwargs)
            if save:
                # Save both the df, and the cache of the keyword arguments
                self.cache[fname] = {'df': df, 'kwargs_hash': hash_kwargs(**kwargs)}
            return df.copy()

        raise ValueError(
            "Either the file doesn't exist, or you specified a filename "
            "that is duplicated across multiple sub-directories in the chosen path. "
            "If the latter is true, please use the full subpath instead."
            )
    

    def save_cached(self, dir="", **kwargs):
        if dir != "":
            if not os.path.exists(dir):
                os.mkdir(dir)
            dir = f"{dir}/"
        for name, item in self.cache.items():
            item['df'].to_csv(f"{dir}{name}.csv", **kwargs)
        

    def save_all(self, dir="", **kwargs):
        # Make directory for custom path
        if dir != "":
            p = ""
            for d in dir.split("/"):
                if p != "":
                    p = f"{p}/{d}"
                else:
                    p = d
                if not os.path.exists(p):
                    os.mkdir(p)

        # Make directories for all sub-paths
        for name in self.datasets:
            fullpath = name.split("/")
            if dir != "":
                fullpath = [dir] + fullpath
            p = None
            if len(fullpath) > 1:
                path = fullpath[:-1]
                p = ""
                for d in path:
                    if p != "":
                        p = f"{p}/{d}"
                    else:
                        p = d
                    if not os.path.exists(p):
                        os.mkdir(p)

        # Save datasets
        for name in self.datasets:
            save = False if name not in self.cache else True
            df = self.load(name, save=save, **kwargs)
            if dir != "":
                df.to_csv(f"{dir}/{name}.csv", **kwargs)
            else:
                df.to_csv(f"{name}.csv", **kwargs)
        

    def refresh_datasets(self):
        res = self.req_files()
        if not res:
            return []

        if res.get("message") == "Not Found":
            raise ValueError("No files found. Likely an invalid data source")
        
        self.truncated_datasets = res.get('truncated', False)

        return [f['path'].removesuffix('.csv').removeprefix(f"{self.path}/")
                    for f in res['tree'] if ".csv" in f['path']]




class DataSource(Source):
    library = None
    sources = None
    if check_internet():
        try:
            library = dict(requests.get(
                "https://raw.githubusercontent.com/ryayoung/datasets/main/chart-tools-default-library.json"
            ).json())
        except Exception as e:
            library = None


    def __init__(self, user=None, repo=None, branch=None, path="", name=None):

        if path.endswith("/"):
            path = path.removesuffix("/")

        if user and repo and branch:
            super().__init__(user, repo, branch, path)
            if name:
                self.name = name
            else:
                self.name = self.repo
            return

        if name:
            if DataSource.library == None:
                raise ValueError("There are no predefined sources to choose from")
            # Create a DataSource by using only the name of a pre-defined one
            source = DataSource.library.get(name, None)
            if not source:
                raise ValueError(f"Unknown source, '{name}'")

            super().__init__(source['u'], source['r'], source['b'], source['p'])
            self.name = name
            return
    


    def display_datasets(self, header=True, trunc=1000):
        if self.datasets == []:
            print("datasets are []")
            return
        if header:
            if self.name != None:
                print(f"Datasets for '{self.name}':")
            if self.name == None:
                print(f"Datasets in '{self.user}/{self.repo}/{self.path}':")
            if len(self.subdirs) > 0:
                print("(refer files inside folders using the full path. Ex: 'folder/file')")
            print("---------------------------")
        
        # Files in base directory
        for file in [f for f in self.datasets if "/" not in f]:
            print(f"  {file}")

        # Files in subdirectories
        count = 0
        for dir in self.subdirs:
            print(f"  {dir}/")
            count += 1
            for f in self.dir_contents(dir):
                count += 1
                if count > trunc: break
                print(f"    {f}")

            if count > trunc: break

        if count > trunc:
            name = self.name if self.name else f"{self.user}/{self.repo}"
            print(f"      ({len(self.datasets)-count} more files in {name})")
    

    def display_subdirs(self):
        print(f"Sub-directories in '{self.user}/{self.repo}/{self.path}'")
        print("---------------------------------------")
        print("  ", end="")
        print(*self.subdirs, sep="\n  ")
    
    @classmethod
    def init_sources(cls):
        if cls.library:
            cls.sources = { k: DataSource(name=k) for k, v in DataSource.library.items() }
            return True
        else:
            return False
    
    @classmethod
    def update_library(cls, new_url):
        if not check_internet():
            return False
        data = None
        if new_url.startswith("https"):
            try:
                data = dict(requests.get(new_url).json())
            except Exception as e:
                print(e)
                return False
        else:
            try:
                with open(new_url) as f:
                    data = json.load(f)
            except Exception as e:
                print(e)
                return False

        if data:
            for key in list(data.keys()):
                if not sorted(list(data[key].keys())) == sorted(['u', 'r', 'b', 'p']):
                    raise ValueError("Wrong library structure. Keys must be ['u', 'r', 'b', 'p']")
            cls.library = data
            cls.init_sources()
            return True
        return False
    
    
        

# --------------------------------------------------------------------------------
def set_library(url):
    DataSource.update_library(url)


def display_sources(srcs) -> None:
    for s in srcs.values():
        print(f" '{s.name}':{(10-len(s.name))*' '}{s.root}")


def display_sources_full(srcs) -> None:
    print("(Use load_data(source_name, filename) to load data)")
    print("(Use load_data(source_name) to see available datasets in source)")
    print("")
    for s in srcs.values():
        if s.datasets == []:
            return
        print(f"'{s.name}'  -  {s.root}")
        print("---------------------------------")
        s.display_datasets(header=False, trunc=15)
        print()


def load_data(source=None, file=None, save=True, **kwargs) -> pd.DataFrame:

    if not DataSource.sources:
        success = DataSource.init_sources()
        if not success:
            return
    srcs = DataSource.sources

    if not source and not file:
        print("Use load_data(source_name, filename) to load dataframe")
        print("Use load_data(source_name) to see all datasets in a source.")
        print("Use load_data('all') to see all datasets.")
        print("---------\nSOURCES:")
        display_sources(srcs)
        return None
    
    if source == 'all' and not file:
        display_sources_full(srcs)
        return None
    
    if not file:
        if source in srcs.keys():
            srcs[source].display_datasets()
            return None
        if hasattr(srcs.get("main", DataSource()), "datasets"):
            if source in srcs.get("main", {}).datasets:
                return srcs['main'].load(source, save, **kwargs)

        print(f"Unknown source, '{source}'")
        return None
        
    if source not in srcs.keys():
        print(f"Unknown source, '{source}'")
        return None
    
    if srcs[source].datasets != []:
        return srcs[source].load(file, save, **kwargs)
