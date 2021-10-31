import sys; args = sys.argv[1:]
#Eshi Kohli
from PIL import Image

def kInitial(pix, mostCommonPixel, knum, w, h):
   #find the unique pixels from the most Common pixels
   ctr = 1
   kMeans = {}
   #1 k
   kMeans[mostCommonPixel] = 1

   mr, mg, mb = mostCommonPixel

   #Find farthest 
   maxd = -1
   maxp = (0, 0, 0)
   for p in pix:
      r, g, b = p
      d = (mr - r) ** 2 + (mg - g) ** 2 + (mb - b) ** 2
      if d > maxd:
         maxd = d
         maxp = (r, g, b)

   ctr += 1 
   #2 k
   kMeans[maxp] = 1
   fr, fg, fb = maxp #farthest from most common pixel
   ir, ig, ib = (mr, mg, mb) #initial most common pixel
   middler, middlrg, middleg = (ir, ig, ib)
  
 
   #Find middle
   while ctr < knum:
      mind = 300
      minp = (-1, -1, -1)
      maxr, maxg, maxb = maxp
      avgr = (mr + maxr)//2
      avgb = (mg + maxg)//2
      avgg = (mb + maxb)//2
      minp = (avgr, avgg, avgb)
   
      ctr += 1
      kMeans[minp] = 1
     
      if ctr < 4:
         maxp = minp
         middler, middlrg, middleg = minp
      elif ctr == 4:
         mr, mg, mb = (middler, middlrg, middleg)
         maxr, maxg, maxb = (fr, fg, fb)
         maxp = (fr, fg, fb)
      else:
         maxp = minp


   return kMeans

def kMeansCalc(pix, kMeans):
   kd = {} #kmeans dict with associated pixels
   #pix is dict of unique r, g, b with the count and coordinates of each rgb  r,g,b : (1, [(x1, y1), (x2, y2)])
   #print(pix)
   for rgbPoint in pix:
      r,g,b = rgbPoint
      mind = -1
      (minr,ming,minb) = (-1, -1, -1)
      for p in kMeans:
  
         kr, kg, kb = p
         d = (r - kr) ** 2 + (g - kg) ** 2 + (b - kb) ** 2
       
         if mind != -1:
            if d < mind:
               mind = d
               (minr,ming,minb) = p
         else:
            mind = d
            (minr,ming,minb) = p
   
      if kd.get((minr,ming,minb)) is None:
         kd.setdefault((minr,ming,minb), [])
     
      #(kr,kg,kb, [(r,g,b, [(x1, y1), (x2, y2)]]
      ct, pixList = pix[rgbPoint]
      kd[(minr,ming,minb)].append((r, g, b,  pixList)) 
   return kd



def check(grid, row, col, num):

   if (row < 0 or row > len(grid) - 1):
      return False

   if (col < 0 or col > len(grid[0]) - 1):
      return False

   if grid[row][col] == num:
      return True
   else:
      return False
     
def floodfill(grid, row, col, num):

   if (row < 0 or row > len(grid) - 1):
      return

   if (col < 0 or col > len(grid[0]) - 1):
      return

   if (grid[row][col] != num):
      return

   q = [] 
   grid[row][col] = -1 
   q.append([row, col]) 

   while len(q) > 0:
      [curRow, curCol] = q[0]
      del q[0]
   
      if (check(grid, curRow - 1, curCol, num) == True):
         grid[curRow - 1][curCol] = -1
         q.append([curRow - 1, curCol])
   
      if (check(grid, curRow + 1, curCol, num) == True):
         grid[curRow + 1][curCol] = -1
         q.append([curRow + 1, curCol])
   
      if (check(grid, curRow, curCol - 1, num) == True):
         grid[curRow][curCol - 1] = -1
         q.append([curRow, curCol - 1])
   
      if (check(grid, curRow, curCol + 1, num) == True):
         grid[curRow][curCol + 1] = -1
         q.append([curRow, curCol + 1])
         
      if (check(grid, curRow - 1, curCol + 1, num) == True):
         grid[curRow - 1][curCol + 1] = -1
         q.append([curRow - 1, curCol + 1])
   
      if (check(grid, curRow -1 , curCol - 1, num) == True):
         grid[curRow - 1][curCol  - 1] = -1
         q.append([curRow - 1, curCol -1])
   
      if (check(grid, curRow + 1, curCol + 1, num) == True):
         grid[curRow + 1][curCol + 1] = -1
         q.append([curRow + 1, curCol + 1])
   
      if (check(grid, curRow + 1, curCol - 1, num) == True):
         grid[curRow+ 1][curCol - 1] = -1
         q.append([curRow + 1, curCol - 1])


def countregions(numarr, num):

   regions = 0
 
   for row in range(len(numarr)):
      for col in range(len(numarr[0])):
         if (numarr[row][col] == num):
            regions += 1
            floodfill(numarr, row, col, num)
   return regions

def kMeansFn(pix, k):
   kMeans = k
   km = {} #initiate for storing previous k means
  
   while not (km == kMeans):
      km = kMeans
      kMeans = {}
     
      #variables to store the the sum of r,g,b for each k mean
      sr = 0
      sg = 0
      sb = 0
      totalcoordlen = 0
   
      #Kmeans dict stores the unique pixels and the coordinate list for each kmean in format (kr,kg,kb, [(r,g,b, [(x1, y1), (x2, y2)]), (r1,g1,b1,[(x,y)])]
      for k, pixels in km.items():
         sr = 0
         sg = 0
         sb = 0
         totalcoordlen = 0
        
         for ps in pixels:
            r,g,b,lst = ps #lst is list of coordinates for the rgb value
            coordlen = len(lst)
         
            sr = sr + r * coordlen
            sg = sg + g * coordlen
            sb = sb + b * coordlen
            totalcoordlen = totalcoordlen + coordlen
           
         sr = sr/totalcoordlen
         sg = sg/totalcoordlen
         sb = sb/totalcoordlen
      
        
         #building new data points for kmean based on the mean
         if kMeans.get((sr, sg, sb)) is None:
            kMeans.setdefault((sr, sg, sb), [])
         kMeans[(sr, sg, sb)].append(1)
      #assign the  pixels  to newly created kmean
      kMeans = kMeansCalc(pix, kMeans)
    
   return kMeans   


   
def main():
    #opening image and setting cariable for K
   im = Image.open(args[1])
   # im.show()
    #print(im.size)
   knum = int(args[0])
  
    #gets all of the pixels
   pixels = im.load()
  
    #get the size of image
   width, height = im.size

    #dictionary to store unique pixels and how many of each pixel there are
   pix = dict()

   mostCommonPixel = (0, 0, 0)
   maxNum = -1
   count = 0
   pixList = []
   pixct = 1
    #looping through pixels to find number of distinct pixels and most common pixel
   c = 0
  
  
   for row in range(width):
      for col in range(height):
         pixList = []
         R, G, B= pixels[row, col]
         #pix is dict of unique r, g, b with the count and coordinates of each rgb  r,g,b : (1, [(x1, y1), (x2, y2)])
         if (R, G, B) in pix:
            pixct, pixList = pix[(R, G, B)]
            pixct += 1
            pixList.append((row, col))
            pix[(R, G, B)] = (pixct, pixList)
         else:
            pixList.append((row, col))
            pix[(R, G, B)] = (1, pixList)
         if pixct > maxNum:
            maxNum, l = pix[(R, G, B)]
            mostCommonPixel = (R, G, B)
            count += 1


    #statistics
   print("Size: " + str(width)+ " x "+str(height))
   print("Pixels: " + str(width*height))
   print("Distinct pixel count: " + str(len(pix)))
   print("Most common pixel: " + str(mostCommonPixel) + " => " + str(count))
   numarr = []
   for i in range(height):
      numarr.append([])
      for j in range(width):
         numarr[i].append(None)

   #  #kmeans statistics that you need to change once you finish the kmeans algorithm
   print("Final means:")

   kMeans = kInitial(pix,  mostCommonPixel, knum, width, height)

   #assigns the pixels to the initialized k means
  
   firstk = kMeansCalc(pix, kMeans)
  
   k = kMeansFn(pix, firstk)
   kctr = 1
   for t,i in k.items():
   
      tr, tg, tb = t
      tr = round(tr)
      tg = round(tg)
      tb = round(tb)
     
      kctr = kctr + 1
      totalpixelct = 0
      for si in i:  
         r,g,b,ll = si
         totalpixelct = totalpixelct + len(ll)
         for coord in ll:
            x,y = coord
            pixels[x,y] = (tr, tg, tb)
            numarr [y][x] = kctr
   
      print(str(kctr - 1) + " : " + str((t)) + " => " + str(totalpixelct))
   regions = ''
  
   for num in range (len(k)):
      regions = regions + str(countregions(numarr, (num + 2))) + ','
   im.show()
   regions = regions[:-1]
   #im = Image.open(args[1])

   print("Region counts: "  + regions)

   #im.save("kmeans/{}.png".format('2022ekohli'), "PNG")
  
if __name__ == '__main__': main()