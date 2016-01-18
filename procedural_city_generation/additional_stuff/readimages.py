def main():
    '''Deprecated. Was used at lange nacht der Wissenschaften to read images and highlight the way they impact the creation of the Strassennetz'''
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    import numpy as np



    img=mpimg.imread('./rawface.jpg')
    img2=np.ndarray(img.shape)

    for x in xrange(img.shape[0]):
        for y in xrange(img.shape[1]):#
            val=img[x][y]

            biggestval=np.argmax(val)
            arr=np.zeros(3)
            arr[biggestval]=1
            img[x][y]=val*arr
            val=val[biggestval]
            val=int(((val-75)*6)+75)
            val=max((250-val), 1)
            val=min(val, 254)
            img2[x][y]=np.array([val, val, val])

    plt.imsave('./Strassennetz/PythonVersion/Regelbilder/face.jpg', img)
    plt.imsave('./Strassennetz/PythonVersion/Bevoelkerungsdichtebilder/face.jpg', img2)

    fig=plt.figure()
    ax=plt.subplot(211)
    ax.imshow(img2)
    ax2=plt.subplot(212)
    ax2.imshow(img)
    plt.show()


    return 0

if __name__ == '__main__':
    main()

