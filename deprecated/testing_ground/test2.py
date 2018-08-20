import os

def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f)) 

a = []
#a.append(absoluteFilePaths('/home/anoush/Dropbox/Khan/Spectral_Plots/'))
print absoluteFilePaths('/home/anoush/Dropbox/Khan/Spectral_Plots/')
#print(a)
path = '/home/anoush/Dropbox/Khan/Spectral_Plots/'

for root, dirs, files in os.walk(path):
    for file in files:
        p=os.path.join(root,file)
        #print p
        #print os.path.abspath(p)
        a.append(os.path.abspath(p))
print(a)
