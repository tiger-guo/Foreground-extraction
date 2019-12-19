from subprocess import Popen

for index in range(100,1700):
    indexStr = str(index)
    fileName = 'Untitled(' + indexStr + ')'
    Popen('matlab -nosplash -nodesktop -r ' + fileName)