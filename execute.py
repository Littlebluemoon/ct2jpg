import subprocess

program_list = ['fork.py', 'slides.py', 'slides_shadow.py',
                'toimage_shadow.py', 'toimage.py', 'pagenum.py',
                'title.py', 'rename.py']

for program in program_list:
    subprocess.call(['python', program])
    print("Finished:" + program)
