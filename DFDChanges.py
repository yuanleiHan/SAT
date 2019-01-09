import os
from tqdm import tqdm
from DFD import genDFD
from diff_parser import parse_diff
import git

python_root_path = os.getcwd()


def filter(project_name):
    project_master_dir = python_root_path + "/" + project_name
    os.chdir(project_master_dir)
    output_dir = "../log/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    os.system("git log  --date=format:'%Y-%m-%d'  --pretty=format:\"%H%  %cd  %s\" > " + output_dir + "/master_log.txt")

    with open(output_dir + "/master_log.txt", encoding="utf-8") as fr:
        log_lines = fr.readlines()

    start = "a74864ec229141784374f1998324d2cbac837295"
    end = "f347d3c59e3304474ca85b17e24261f127b27282"
    flag = False
    lines = []
    logs = []
    for line in log_lines:
        line = line.split()
        commit_id, date, log = line[0], line[1], " ".join(line[2:])
        if commit_id == start:
            flag = True
        if not flag:
            continue
        lines.append(commit_id)
        logs.append(log)
        if commit_id == end:
            flag = False

    return list(zip(lines, logs))


def DFD_continuous():
    project_name = "flask"
    master_id = "a74864ec229141784374f1998324d2cbac837295"
    os.chdir(python_root_path)
    os.chdir(project_name)
    os.system("git reset --hard {}".format(master_id))
    repo = git.Repo(python_root_path + '/' + project_name)
    filter_lines = filter(project_name)
    old_sha = master_id
    old_DFD = genDFD(python_root_path + '/' + project_name)
    changes = []
    for commit_id, log in tqdm(filter_lines):
        new_sha = commit_id
        os.system("git reset --hard --quiet {}".format(commit_id))
        new_DFD = genDFD(python_root_path + '/' + project_name)
        diff = repo.git.diff(new_sha, old_sha)
        cm_info=parse_diff(diff)
        cnt = 0
        for f in cm_info:
            filename = f.src_file
            if filename[-3:] != '.py':
                continue
            if filename in new_DFD.keys():
                for funcname, affected_new in new_DFD[filename].items():
                    if filename not in old_DFD.keys() or funcname not in old_DFD[filename].keys():
                        affected_old = set()
                    else:
                        affected_old = old_DFD[filename][funcname]
                    cnt += len(affected_new|affected_old) - len(affected_new&affected_old)
            if filename in old_DFD.keys():
                for funcname, affected_old in old_DFD[filename].items():
                    if filename not in new_DFD.keys() or funcname not in new_DFD[filename].keys():
                        affected_new = set()
                    else:
                        affected_new = new_DFD[filename][funcname]
                    cnt += len(affected_new|affected_old) - len(affected_new&affected_old)
        changes.append((new_sha, cnt, log))
        old_sha = new_sha
        old_DFD = new_DFD

    master_id = "a74864ec229141784374f1998324d2cbac837295"
    os.chdir(python_root_path)
    os.chdir(project_name)
    os.system("git reset --hard {}".format(master_id))
    os.chdir(python_root_path)

    with open("output/result_continuous.txt", 'w', encoding = 'utf-8') as f:
        for change in changes:
            f.write(change[0]+ ' ' + str(change[1]) + ' ' + change[2] +"\n")

def DFD_func():
    project_name = "flask"
    master_id = "a74864ec229141784374f1998324d2cbac837295"
    os.chdir(python_root_path)
    os.chdir(project_name)
    os.system("git reset --hard {}".format(master_id))
    repo = git.Repo(python_root_path + '/' + project_name)
    old_sha = master_id
    old_DFD = genDFD(python_root_path + '/' + project_name)
    versions = {'v1.0.2': 'dfd3619d6f8796d48fc4e32f819cec9e8aa59156',
                'v1.0.1': 'a15795c99e24c50e2dc85393a8904f3093742646',
                'v1.0.0': '291f3c338c4d302dbde01ab9153a7817e5a780f5',
                'v0.12.0': '1042d9d23f3c61f4474aea568a359337cf450fab',
                'v0.11.0': '13e6a01ac86f9b8c0cad692d5e5e8d600674fb6d',
                'v0.10.0': '3b9574fec988fca790ffe78b64ef30b22dd3386a',
                'v0.9.0': 'ee3e251f9eb557721517faa6d06a6addd48ebc24',
                'v0.8.0': 'd5e10e4685f54dde5ffc27c4f55a19fb23f7a536',
                'v0.7.0': 'fb1482d3bb1b95803d25247479eb8ca8317a3219',
                'v0.6.0': '5cadd9d34da46b909f91a5379d41b90f258d5998',
                'v0.5.0': '4c937be2524de0fddc2d2f7f39b09677497260aa'}

    changes = []
    for version, commit_id in tqdm(versions.items()):
        new_sha = commit_id
        os.system("git reset --hard --quiet {}".format(commit_id))
        new_DFD = genDFD(python_root_path + '/' + project_name)
        diff = repo.git.diff(new_sha, old_sha)
        cm_info=parse_diff(diff)
        cnt = 0
        for f in cm_info:
            filename = f.src_file
            if filename[-3:] != '.py':
                continue
            if filename in new_DFD.keys():
                for funcname, affected_new in new_DFD[filename].items():
                    if filename not in old_DFD.keys() or funcname not in old_DFD[filename].keys():
                        affected_old = set()
                    else:
                        affected_old = old_DFD[filename][funcname]
                    cnt += len(affected_new|affected_old) - len(affected_new&affected_old)
            if filename in old_DFD.keys():
                for funcname, affected_old in old_DFD[filename].items():
                    if filename not in new_DFD.keys() or funcname not in new_DFD[filename].keys():
                        affected_new = set()
                    else:
                        affected_new = new_DFD[filename][funcname]
                    cnt += len(affected_new|affected_old) - len(affected_new&affected_old)
        changes.append((new_sha, cnt, version))
        old_sha = new_sha
        old_DFD = new_DFD

    master_id = "a74864ec229141784374f1998324d2cbac837295"
    os.chdir(python_root_path)
    os.chdir(project_name)
    os.system("git reset --hard {}".format(master_id))
    os.chdir(python_root_path)

    with open("output/result_func.txt", 'w', encoding = 'utf-8') as f:
        for change in changes:
            f.write(change[2] + ' ' + change[0]+ ' ' + str(change[1]) + "\n")


if __name__ == '__main__':
    DFD_func()
    DFD_continuous()
