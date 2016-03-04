__author__ = 'zhenanye'
# coding = utf8
import filesystem

fs = filesystem.FileSystem(1)

print fs.read_folder(1)

fs.create_folder(2, 'thirdfolder')

fs.delete_file(3)

#fs.create_file(2, 'insertfile.txt', 'content')