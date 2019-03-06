from skimage import io, morphology
from pylab import *
import skimage
from scipy import ndimage as ndi
from skimage.filters import sobel
from skimage import measure
from skimage.draw import circle
from skimage.util import img_as_ubyte
from skimage.filters import threshold_isodata, threshold_yen, threshold_sauvola
from skimage.morphology import closing, square


def zrob(image, image1, i, j):

    # Stworzenie trzech różnych progowań dla czarno-białego obrazka
    thresh = threshold_isodata(image)
    th_sa = threshold_sauvola(image)
    th_ye = threshold_yen(image)

    # Porównanie progowań z obrazkiem i wyznaczenie konturów
    binary_is = closing(image > thresh, square(3))
    binary_sa = (image > th_sa)
    binary_ye = (image > th_ye)

    # Połączenie metod progowania za pomocą OR
    binary1 = logical_or(binary_ye, binary_sa)
    binary2 = logical_or(binary_ye, binary_is)
    binary3 = logical_or(binary_is, binary_sa)

    # Dla tych trzed metod zostaje wygenerowany sobel (wyznaczanie krawędzi), zamknięcie konturów i ich wypełnienie,
    # a następnie oczyszczenie obrazu z mniejszych elementów
    binary1 = sobel(binary1)
    wypelni1 = ndi.binary_closing(binary1)
    wypelni1 = ndi.binary_fill_holes(wypelni1)
    wyczysc1 = morphology.remove_small_objects(wypelni1, 1000)
    x = 0

    binary2 = sobel(binary2)
    wypelni2 = ndi.binary_closing(binary2)
    wypelni2 = ndi.binary_fill_holes(wypelni2)
    wyczysc2 = morphology.remove_small_objects(wypelni2, 1000)
    y = 0

    binary3 = sobel(binary3)
    wypelni3 = ndi.binary_closing(binary3)
    wypelni3 = ndi.binary_fill_holes(wypelni3)
    wyczysc3 = morphology.remove_small_objects(wypelni3, 1000)
    z = 0

    # Tworzenie listy a do zbierania informacji o ilości wygenerowanych konturów
    a = []

    # Każdy z tych wygenerowanych obrazów jest sprawdzany pod względem ilości konturów, które wygenerował
    contours = measure.find_contours(wyczysc1, 0.5, fully_connected='high')
    for n, contour in enumerate(contours):
        x = n
    a.append(x)

    contours = measure.find_contours(wyczysc2, 0.5, fully_connected='high')
    for n, contour in enumerate(contours):
        y = n
    a.append(y)

    contours = measure.find_contours(wyczysc3, 0.5, fully_connected='high')
    for n, contour in enumerate(contours):
        z = n
    a.append(z)

    print(a)
    # Wybranie najmniejszej ilości konturów
    wybierz = min(a)

    # Sprawdzenie, którą metodą została wykonana metoda o najmniejszej ilości konturów
    if y == wybierz:
        contours = measure.find_contours(wyczysc2, 0.5, fully_connected='high')
    elif x == wybierz:
        contours = measure.find_contours(wyczysc1, 0.5, fully_connected='high')
    else:
        contours = measure.find_contours(wyczysc3, 0.5, fully_connected='high')

    # Generowanie ostatecznych konturów z wybranej metody
    for n, contour in enumerate(contours):
        # Rysowanie konturu w metodzie
        ax[i, j].plot(contour[:, 1], contour[:, 0], linewidth=1)
        # Narysowanie kółka w centrum konturu obliczonego ze średnich wartości x i y
        rr, cc = skimage.draw.circle(int(sum(contour[:, 0]) / len(contour[:, 0])), int(sum(contour[:, 1]) /
                                                                                       len(contour[:, 1])), radius=6)
        # Zmienienie tych współrzędnych kółka dla kolorowego obrazka
        image1[rr, cc] = 255
        print(n)

    # Nałożenie kolorowego obrazka
    ax[i, j].imshow(image1, interpolation='nearest')
    ax[i, j].axis('image')
    ax[i, j].set_xticks([])
    ax[i, j].set_yticks([])


if __name__ == "__main__":

    # Ustawienie wartości dla pierwszego obrazka i ustawienia jego rozmiaru i ilości subplotów
    i = 0
    j = 0
    fig, ax = plt.subplots(4, 4)
    fig.set_figheight(45)
    fig.set_figwidth(45)

    # Wczytywanie obrazków ze strony, (image1) wczytujemy jako normalny obrazek do tła, a (image) jako czarno-biały do
    # wyznaczania konturów samolotów, wywołanie funkcji i zmiana subplotu przy kolejnym obrazku
    image1 = io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot00.jpg")
    image = img_as_ubyte(io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot00.jpg",
                                   as_gray=True))
    zrob(image, image1, i, j)

    i = 0
    j = 1
    image1 = io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot01.jpg")
    image = img_as_ubyte(io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot01.jpg",
                                   as_gray=True))
    zrob(image, image1, i, j)

    i = 0
    j = 2
    image1 = io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot02.jpg")
    image = img_as_ubyte(io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot02.jpg",
                                   as_gray=True))
    zrob(image, image1, i, j)

    i = 0
    j = 3
    image1 = io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot03.jpg")
    image = img_as_ubyte(io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot03.jpg",
                                   as_gray=True))
    zrob(image, image1, i, j)

    i = 1
    j = 0
    image1 = io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot11.jpg")
    image = img_as_ubyte(io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot11.jpg",
                                   as_gray=True))
    zrob(image, image1, i, j)

    i = 1
    j = 1
    image1 = io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot05.jpg")
    image = img_as_ubyte(io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot05.jpg",
                                   as_gray=True))
    zrob(image, image1, i, j)

    i = 1
    j = 2
    image1 = io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot07.jpg")
    image = img_as_ubyte(io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot07.jpg",
                                   as_gray=True))
    zrob(image, image1, i, j)

    i = 1
    j = 3
    image1 = io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot08.jpg")
    image = img_as_ubyte(io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot08.jpg",
                                   as_gray=True))
    zrob(image, image1, i, j)

    i = 2
    j = 0
    image1 = io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot09.jpg")
    image = img_as_ubyte(io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot09.jpg",
                                   as_gray=True))
    zrob(image, image1, i, j)

    i = 2
    j = 1
    image1 = io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot10.jpg")
    image = img_as_ubyte(io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot10.jpg",
                                   as_gray=True))
    zrob(image, image1, i, j)

    i = 2
    j = 2
    image1 = io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot17.jpg")
    image = img_as_ubyte(io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot17.jpg",
                                   as_gray=True))
    zrob(image, image1, i, j)

    i = 2
    j = 3
    image1 = io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot12.jpg")
    image = img_as_ubyte(io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot12.jpg",
                                   as_gray=True))
    zrob(image, image1, i, j)

    i = 3
    j = 0
    image1 = io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot13.jpg")
    image = img_as_ubyte(io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot13.jpg",
                                   as_gray=True))
    zrob(image, image1, i, j)

    i = 3
    j = 1
    image1 = io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot14.jpg")
    image = img_as_ubyte(io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot14.jpg",
                                   as_gray=True))
    zrob(image, image1, i, j)

    i = 3
    j = 2
    image1 = io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot15.jpg")
    image = img_as_ubyte(io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot15.jpg",
                                   as_gray=True))
    zrob(image, image1, i, j)

    i = 3
    j = 3
    image1 = io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot16.jpg")
    image = img_as_ubyte(io.imread("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/planes/samolot16.jpg",
                                   as_gray=True))
    zrob(image, image1, i, j)

    # Zapis i wyświetlenie
    fig.savefig("samoloty.pdf")
    fig.savefig("samoloty.png")

    plt.show()
