import os


class cutRequirements:

    def __init__(self,registry_mirror = 'https://pypi.tuna.tsinghua.edu.cn/simple',path='.'):
        self.path = path
        self.files = []
        self.registry_mirror = registry_mirror
        for dirpath, dirnames, filenames in os.walk(self.path):
            for filename in filenames:
                self.files.append(os.path.join(dirpath, filename))
        result = os.popen(f'pip3 freeze').read().split('\n')
        self.env_packages_name = []
        self.env_packages_version = []
        self.req_packages = []
        for r in result:
            self.env_packages_name.append(r.split('==')[0])
            self.env_packages_version.append(r.split('==')[-1])
        self.totalText = ''
        for path in self.files:
            # print(path)
            if path.endswith('.py'):
                with open(path, encoding='utf-8') as file_obj:
                    for i in file_obj.readlines():
                        # print(i)
                        self.totalText += i

    def get_req_packages(self):
        arr = self.totalText.split('\n')
        for i in arr:
            if i.startswith('from'):
                pack = i.split(' ')
                package = pack[1].split('.')[0]
                try:
                    package = package + "==" + self.env_packages_version[self.env_packages_name.index(package)]
                    if package in self.req_packages:
                        pass
                    else:
                        self.req_packages.append(package)
                except:
                    pass
            elif i.startswith('import'):
                pack = i.split(' ')
                pack.remove('import')
                for package in pack:
                    package = package.replace(',', '')
                    package = package.replace('\n', '')
                    try:
                        package = package + "==" + self.env_packages_version[self.env_packages_name.index(package)]
                        if package in self.req_packages:
                            pass
                        else:
                            self.req_packages.append(package)
                    except:
                        pass
            else:
                pass

    def get_download_text(self):
        self.get_req_packages()
        with open('require_packages.txt','w') as rp:
            for package in self.req_packages:
                rp.write(f'pip install {package} -i {self.registry_mirror}\n')
                # print(f'pip install {package} -i {self.registry_mirror}')

    def get_current_folder_packages_info(self):
        with open('current_folder_packages_info.txt','w') as rp:
            for package in self.req_packages:
                rp.write(f'{package}\n')

if __name__ == '__main__':
    req_packages1 = cutRequirements()
    req_packages1.get_download_text()
