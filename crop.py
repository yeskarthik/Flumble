import Image

img=Image.open("/home/karthik/Pictures/mestaring.jpg");

l=img.size[0]
b=img.size[1]

l=l/5
b=b/5
i=0

fname='/home/karthik/Images/cropped'

while(i<5):
    j=0
    while(j<5):
        cropp=img.crop((i*l,b*j,l*i+l,b*j+b))
        cropp.save(fname+str(i)+str(j),'PNG')
        j+=1
    i+=1

