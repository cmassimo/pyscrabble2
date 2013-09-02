class CombinationGenerator(object):
    factorials = { 0:1L, 1:1L, 2:2L, 3:6L, 4:24L, 5:120L,
        6:720L, 7:5040L, 8:40320L, 9:362880L, 10:3628800L,
        11:39916800L, 12:479001600L, 13:6227020800L,
        14:87178291200L, 15:1307674368000L}

    def __init__(self, domain, choose):
        self.domain = domain
        self.choose = choose
        self.total_combinations = self.factorials[self.domain] / (self.factorials[self.choose] * self.factorials[self.domain - self.choose])
        self.combinations_left = self.total_combinations
        self.data = range(0, self.choose)

    def get_next(self):
        # print '--- dentro get_next:'
        # print self.data
        if self.combinations_left == self.total_combinations:
            self.combinations_left = self.combinations_left - 1L
        else:
            i = self.choose - 1
            # print "%d == %d - %d + %d" % (self.data[i], self.domain, self.choose, i)
            while self.data[i] == self.domain - self.choose + i:
                # print self.data[i] == self.domain - self.choose + i
                i = i - 1
            # print "self.data[%d] = %d + 1" % (i, self.data[i])
            self.data[i] = self.data[i] + 1
            for j in range(i+1, self.choose):
                # print "self.data[%d] = %d + %d - %d" % (j, self.data[i], j, i)
                self.data[j] = self.data[i] + j - i
            self.combinations_left = self.combinations_left - 1L
            
        # print self.data
        return self.data

    def has_next(self):
        return not (self.combinations_left == 0)