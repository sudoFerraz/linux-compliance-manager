import matplotlib.pyplot as plt

#x = [2,4,6,8,10]
#y = [6,7,8,2,4]

#plt.bar(x, y, label='bars1', color='r')
#x2 = [1,3,5,9,11]
#y2 = [7,8,2,4,2]
#plt.bar(x2,y2, label='Bars2')

#population_ages = [22,55,62,45,21,22,34,42,42,4,99,102,110,120,121,133,111,48]
#ids = [x for x in range(len(population_ages))]

#bins = [0,10,20,30,40,50,60,70,80,90,100,110,120,130]

#plt.hist(population_ages, bins, histtype='bar', rwidth=0.8)

#x = [1,5,7,8,4,5,7,4,5,66]
y = [4,7,8,5,4,5,4,44,4,17]
gameswon = ['eu','vc','ele','nos','eles','elas','ela','tu','vos','todos']

#plt.scatter(x,y,label='scats', color='c')
plt.pie(y, labels=gameswon)

plt.xlabel('x')
plt.ylabel('y')
plt.title('Interesting Graph')
plt.legend()


plt.show()
