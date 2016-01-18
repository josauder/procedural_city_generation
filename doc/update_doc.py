
def main():



    l=len("procedural_city_generation")+1
    import os, sys

    os.system("sphinx-apidoc -o . ..")

    for x in os.listdir(os.getcwd()):
        if x.endswith(".rst"):
            print x
            x2=x
            if "procedural_city_generation.procedural_city_generation" in x:
                x2=x[l:]
                os.system("mv "+x+" "+x2)

            with open(x2, 'r') as f:
                filecontent=f.read()

            filecontent=filecontent.replace("procedural_city_generation.procedural_city_generation", "procedural_city_generation")
            with open(x2, 'w') as f:
                f.write(filecontent)

    script=[
    "make html",
    "rm -R procedural_city_generation",
    "sudo git clone https://github.com/josauder/procedural_city_generation.git --branch gh-pages",
    "sudo rm -R ./procedural_city_generation/*",
    "mv _build/html/* procedural_city_generation"]
    for command in script:
        os.system(command)
    os.chdir("procedural_city_generation")
    os.system("touch .nojekyll")
    os.system("git add --all")
    os.system("git commit -m \" Automatic Doc Update\" ")
    os.system("git push")
    os.chdir("..")
    os.system("sudo rm -R procedural_city_generation")




    return 0

if __name__ == '__main__':
    main()

