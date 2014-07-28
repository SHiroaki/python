# -*- coding: utf-8 -*-

import time
import random
import math

people = [('Seymoour', 'BOS'),
          ('Franny', 'DAL'),
          ('Zppey', 'CAK'),
          ('Walt', 'MIA'),
          ('Buddy', 'ORD'),
          ('Les', 'OMA')]

#ニューヨークの空港（ラガーディア）
destination = 'LGA'

flights = {}

for line in file('schedule.txt'):
    origin, dest, depart, arrive, price=line.strip().split(',')
    #辞書オブジェクト.setdefault(キー, 値)
    flights.setdefault((origin,dest), [])

    #リストにフライトの詳細を追加
    flights[(origin, dest)].append((depart, arrive, int(price)))

#for k,v in flights.items():
 #   print k,v

def getminutes(t):
    """ある時刻が一日の中で何分目になるのか計算する"""

    x = time.strptime(t, '%H:%M')
    return x[3]*60+x[4]

def printschedule(r):
    """解をもとにフライトを出力する"""

    for d in xrange(len(r)/2):
        name = people[d][0]
        origin = people[d][1]
        out = flights[(origin, destination)][int(r[d*2])]
        ret = flights[(destination, origin)][int(r[d*2+1])]
        print '%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (name, origin,out[0], out[1], out[2],
                                                      ret[0], ret[1], ret[2])

def schedulecost(sol):
    """コスト関数
    時間によってエラーになる可能性あり。randintの影響か？
    solがNoneになったらスコア最悪にする"""
    
    totalprice = 0
    latestarrival = 0
    earliestdep = 24*60
    
    if sol == None:
        return 99999999

    for d in xrange(len(sol)/2):
        #行き(outbound)と帰り(return)のフライトを得る
        origin=people[d][1] #dさんがどの空港から出発するか
        #dがLAG空港に行くフライトを探す
        outbound = flights[(origin, destination)][int(sol[d*2])] 
        #ｄさんがLAG空港からもどるフライト
        returnf = flights[(destination, origin)][int(sol[d*2+1])]
        
        #運賃総額total priceは出立便と帰宅便すべての運賃
        totalprice += outbound[2]
        totalprice += returnf[2]

        #最も遅い到着時刻と最も早い出発を記録
        if latestarrival < getminutes(outbound[1]):
            latestarrival = getminutes(outbound[1])

        if earliestdep > getminutes(returnf[0]):
            earliestdep = getminutes(returnf[0])

    #最後の人が到着するまで全員空港で待機
    #帰りも空港にみんなできて自分の便の出発を待つ
    totalwait = 0
    for d in xrange(len(sol)/2):
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[d*2])] 
        returnf = flights[(destination, origin)][int(sol[d*2+1])]
        totalwait += latestarrival - getminutes(outbound[1])
        totalwait += getminutes(returnf[0]) - earliestdep

    #レンタカー料金追加
    if latestarrival < earliestdep:
        totalprice += 50
        
    return totalprice + totalwait

def randomoptimize(domain, costf):

    best = 99999999
    bestr = None

    for i in xrange(1000):
        #無作為解の生成
        r = [random.randint(domain[i][0], domain[i][1]) 
             for i in xrange(len(domain))]

    
        #コストの取得
        cost = costf(r)

        #最良解との比較
        if cost < best:
            best = cost
            bestr = r

    return r

def hillclimb(domain, costf):
    #無作為解の生成
    sol = [random.randint(domain[i][0], domain[i][1]) 
               for i in xrange(len(domain))]
    print sol
    #main loop
    while 1:
        #近傍解リストの作成
        neihbors = []
        for j in xrange(len(domain)):
            #各方向に１ずつずらす
            if sol[j] > domain[j][0]:
                neihbors.append(sol[0:j]+[sol[j]-1]+sol[j+1:])
            if sol[j] < domain[j][1]:
                neihbors.append(sol[0:j]+[sol[j]+1]+sol[j+1:])

        #近傍解の中のベストを探す
        current = costf(sol)
        best = current
        
        for j in xrange(len(neihbors)):
            cost = costf(neihbors[j])
            if cost < best:
                best = cost
                sol = neihbors[j]

        #改善が得られなければそれが最適解
        if best == current:
            break

    return sol

def geneticoptimize(domain, costf, popsize=50, step=1, 
                    mutprob=0.2, elite=0.2, maxiter=100):

    #突然変異の操作
    def mutate(vec):
        i = random.randint(0, len(domain)-1)
        if random.random() < 0.5 and vec[i] > domain[i][0]:
            return vec[0:i]+[vec[i]-step]+vec[i+1:]
        elif vec[i] < domain[i][1]:
            return vec[0:i]+[vec[i]+step]+vec[i+1:]

    #交叉の操作
    def crossover(r1, r2):
        i = random.randint(1, len(domain)-2)
        return r1[0:i]+r2[i:]

    #初期個体群の生成
    pop = []
    for i in xrange(popsize):
        vec = [random.randint(domain[i][0], domain[i][1])
               for i in xrange(len(domain))]

        pop.append(vec)

    #各世代の勝者数
    topelite = int(elite*popsize)
    
    #main loop
    for i in xrange(maxiter):

        scores = [(costf(v), v) for v in pop] #適応度を計算
        scores.sort() #適応度でソート
        ranked = [v for (s,v) in scores]

        #純粋な勝者
        pop = ranked[0:topelite]
        
        #勝者に突然変異や交配を行ったものを追加
        while len(pop) < popsize:
            if random.random() < mutprob:
                #突然変異
                c = random.randint(0, topelite) #0以上、topelite以下の整数を発生
                pop.append(mutate(ranked[c])) #ｃ番目の個体の任意番目の要素を１進めるか１戻す
            else:
                #交叉
                c1 = random.randint(0, topelite)
                c2 = random.randint(0, topelite)
                pop.append(crossover(ranked[c1], ranked[c2]))

        #現在のベストスコア
        print scores[0][0]

    return scores[0][1]

if __name__ == "__main__":
    domain = [(0,9)]*(len(people)*2)
    s = geneticoptimize(domain, schedulecost)
    print printschedule(s)
