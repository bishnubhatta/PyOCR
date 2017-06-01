#Install Pillow --- pip install pillow
#Install pytesseract --- pip install pytesseract
#Install tesseract-ocr  ---- sudo apt-get install tesseract-ocr (Linux) or
# https://osdn.net/projects/sfnet_tesseract-ocr-alt/downloads/tesseract-ocr-setup-3.02.02.exe/ (Windows)
#Install ghostscript for PDF to image conversion --- pip install ghostscript
#Install Ghostscript DLL for windows 64BIT
# https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs921/gs921w64.exe
# Improving the quality of the output:
# https://github.com/tesseract-ocr/tesseract/wiki/ImproveQuality
#THIS IS GOOD FOR PRINTED DOCUMENTS AND NOT GOOD FOR HANDWRITTEN OR DISTORTED CAPTCHA

class PyOCR:
    def __init__(self):
        self.lang='eng'
        self.dir_path='C:/PyOCR/'
        self.temp_dir = 'C:/PyOCR/Temp/'
        self.file_list=[]

    def read_files_from_disk(self,basedir,file_ext):
        import os
        file_list=[]
        for (dirpath, dirnames, filenames) in os.walk(basedir):
            for filename in filenames:
                if os.path.splitext(filename)[1] in file_ext:
                    file_list.append(filename)
        print file_list
        return file_list

    def pdf2jpeg(self,pdf_list):
        import ghostscript
        import os
        for file in pdf_list:
            basename = file.split(".")[0]
            print basename
            print os.path.join(self.temp_dir , basename+"%03d.jpeg")
            args = ["pdf2jpeg", # actual value doesn't matter
                "-dNOPAUSE",
                "-sDEVICE=jpeg",
                "-r144",
                "-sOutputFile=" + os.path.join(self.temp_dir , basename+"%03d.jpeg"), #%03.d will increment the file name
                os.path.join(self.dir_path, file)]
            ghostscript.Ghostscript(*args)

    def convert_image_to_string(self,basedir,jpeg_list,lang):
        try:
            from  PIL import Image,ImageEnhance
            import pytesseract as pt
            for jpeg_file in jpeg_list:
                file_name=jpeg_file.split(".")[0]+'.txt'
                with open(self.dir_path + file_name , 'a') as f:
                    im=Image.open(basedir+jpeg_file)
                    #https://www.youtube.com/watch?v=NdtRROZWjwA
                    # nx,ny=im.size
                    # im2=im.resize((int(nx*5),int(ny*5)),Image.BICUBIC)
                    # im2.save(basedir+"Temp/"+jpeg_file)
                    # img=Image.open(basedir+"Temp/"+jpeg_file)
                    # enh=ImageEnhance.Contrast(im)
                    # enh.enhance(1.3).show("30% more contrast")
                    # img=img.convert("RGBA")
                    # pixdata =img.load()
                    f.write(pt.image_to_string(im,lang=lang))
        except Exception, e1:
            print str(e1)

    def cleanup_temp_dir(self):
        try:
            import os
            for file in os.listdir(self.temp_dir):
                filepath= os.path.join(self.temp_dir, file)
                if os.path.isfile(filepath):
                    os.unlink(filepath)
        except Exception as e:
            print(e)

    def enhance_image(self):
        print "Yet to be coded!!!Need help here"

pcr= PyOCR()
sel=int(raw_input("\nWhat type of files you want to convert? "
                  "Press 1 for PDF, Press 2 for JPG, Press 3 for Enhance images, Press any other key to Exit\n"))
if sel not in [1,2,3]:
    print "You selected to Exit. Have a nice day!!!"
    exit()
elif sel== 1:
    file_list= pcr.read_files_from_disk(pcr.dir_path,['.pdf'])
    pcr.cleanup_temp_dir()
    pcr.pdf2jpeg(file_list)
    jpeg_list= pcr.read_files_from_disk(pcr.temp_dir,['.jpeg'])
    pcr.convert_image_to_string(pcr.temp_dir,jpeg_list,'eng')
    pcr.cleanup_temp_dir()
elif sel == 2:
    file_list= pcr.read_files_from_disk(pcr.dir_path,['.jpg','.png'])
    pcr.cleanup_temp_dir()
    pcr.convert_image_to_string(pcr.dir_path,file_list,'eng')
    pcr.cleanup_temp_dir()
else:
    pcr.enhance_image()