toolik8 = ['20170901-0844-0909-TLK-INT', '20170915-0915-0942-TLK-INT']
toolik9 = ['20180415-0759-0818-TLK-INT', '20180421-0732-0753-TLK-INT', '20180421-0806-0833-TLK-INT', '20180426-0937-0951-TLK-INT', '20180506-0713-0746-TLK-INT', '20180507-0653-0801-TLK-INT']


script = open('scp.txt', 'w')

i = 0
while i <= (len(toolik8) - 1):
    command = 'scp canopus@einstein.dartmouth.edu:/jwl1/toolik8/rawdata_files/' + toolik8[i] + '.dat ' + toolik8[i] + '.dat'
    script.write(command + '\n')
    i += 1

j = 0
while j <= (len(toolik9) - 1):
    command = 'scp canopus@einstein.dartmouth.edu:/jwl1/toolik9/rawdata_files/' + toolik9[j] + '.dat ' + toolik9[j] + '.dat'
    script.write(command + '\n')
    j += 1

script.close()
