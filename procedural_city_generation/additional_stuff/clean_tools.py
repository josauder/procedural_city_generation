import os
path_to_source= os.getcwd()[0:-len("/additional_stuff")]

def listfiles(path):

    filelist=[]

    liste=os.listdir(path)
    counter=0
    for x in liste:
        if not os.path.isdir(path+"/"+x):
            filelist.append(path+"/"+x)
        else:
            filelist.extend(listfiles(path+"/"+x))
    return filelist



def clean_pyc_files(path):
    pyc_files= [x for x in listfiles(path) if x.endswith(".pyc")]
    for pyc in pyc_files:
        os.system("rm -f "+pyc)
    return 0

def find_readable_files(path, suffixes=[".py", ".conf"]):
    """

    """
    allfiles=listfiles(path)
    readables=[]
    for somefile in allfiles:
        if any([somefile.endswith(x) for x in suffixes]) and not os.path.isdir(somefile):
            readables.append(somefile)
    return readables


def find_in_text(path, tofind="TODO"):
    """
    Searches the entire source code in the path for tofind.
    Useful for finding TODOS or missing translations. Like grep,
    nobody knows why this function was built. Prints filename, line number
    and line for each occurence.

    Parameters
    ----------
    path : String
        path in which all files are searched for tofind
    tofind : String
        String which is supposed to be found in source.


    """
    allfiles=find_readable_files(path)
    for somefile in allfiles:
        with open(somefile, 'r') as f:
            s=f.readlines()
        todos=[]
        for i in range(len(s)):
            if tofind in s[i]:
                todos.append([i, s[i].strip()])
        if len(todos)>0:
            print("\n"+somefile)
            for x in todos:
                print( "Line: ", x[0], " \"", x[1], "\"")
    return 0

def add_license_text(files):
    with open(os.path.dirname(path_to_source)+"/licenceheader.txt", 'r') as f:
        licencetext=f.read()

    for fi in files:
        with open(fi, 'r') as f:
            content=f.read()
        if "<info>" in content and "</info>" in content:
            lower=content.find("<info>")
            upper=content.find("</info>")+7

            content= content[:lower]+licencetext[2:-1]+content[upper:]

        elif "<info>" in content or "</info>" in content:
            print("Error, ", fi , " was ommitted from adding licensing header, check if <info> or </info> tag are falsely placed")
        else:
            content=licencetext + "\n" + content

        with open(fi, 'w') as f:
            f.write(content)
    return 0

def find_imports(path):
    all_imports=[]
    for f in find_readable_files(path):
        with open(f, 'r') as g:
            s=g.readlines()
        all_imports.extend([x for x in s if "import " in x and "procedural_city_generation" not in x])

    new_all_imports=set([])
    for imp in all_imports:
        imp=imp.split(" as ")[0]
        imp=imp.replace("import", "").replace("from", "").replace("\t", "").replace("\n", "").replace("\r", "")
        imp=".".join([x for x in imp.split(" ") if x is not ""])
        new_all_imports.add(imp)
    print(new_all_imports)


