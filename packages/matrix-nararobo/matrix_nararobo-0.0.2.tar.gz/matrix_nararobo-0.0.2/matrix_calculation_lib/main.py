

class matrix_caluculation():
    #余因子展開
    def __init__(self):
        self.matrix = [[2,3,4],[1,6,9],[2,7,9]]
        self.indent = []
        self.matrix_2 = []
        self.indent_i = 0
        self.matrix_next =self.matrix
        
    def Calculation_matrix(self,i,matrix_):
        
        matrix_1 = []
        flag_if=False
        c_i=0
        
        for c in range(0,len(matrix_)):
        
            if flag_if ==True:   
        
                matrix_1.append([])
                
            flag_if = True
            
        
        for m in range(0,len(matrix_)):
            
            for c in range(0,len(matrix_)):
                
                if m != 0 and c != i:
                    
                    matrix_1[c_i].append(matrix_[c][m])
                    c_i += 1
            c_i = 0        
        
        return matrix_1

    #展開したものを配列に格納    

    def Calculation(self,matrix_):
        matrix_1 = []
        indent = []
        for i in range(0,len(matrix_)):

            indent.append(matrix_[i][0])
            matrix_1 += self.Calculation_matrix(i,matrix_)
            
        return indent,matrix_1

    def main_caluculation(self):
        
        #初期化
        self.indent = []
        self.matrix_2 = []
        self.indent_i = 0
        self.matrix_next =self.matrix
        
        #展開を行列式がなくなるまで続ける
        
        while(1):
            
            matrix_3 = []

            
            number = [len(v) for v in self.matrix]
            matrix_number = len(self.matrix)/number[0]
            
            if 1 == number[1]:
                break
            
            for i in range(0,int(matrix_number)):
                
                matrix_2 = []
                
                for m in range(0,number[0]):
                    
                    matrix_2.append(self.matrix[number[0]*i+m])
                    
                indent_1,matrix_1 = self.Calculation(matrix_2)
                
                self.indent.append([])
                self.indent[self.indent_i].append(indent_1)

                
                matrix_3 += matrix_1
                
            
            self.matrix = matrix_3   
            
            self.indent_i += 1
            matrix_2 = []
            
        #最終計算
        number = [len(v) for v in self.matrix_next]
        calculation_number = number[0] - 1
        indent_x = []
        for i in range(0,calculation_number):
            indent_x.append(self.indent[i])

        self.indent = indent_x


        for i in range(0,calculation_number):
            
            indent_x = self.indent[calculation_number-1-i]
            number = [len(v) for v in indent_x]
            c = calculation_number-1-i


            
            matrix_i = []
            
            for m in range(0,len(self.indent[c])):
                
                matrix_l = []
                number_l = [len(v) for v in self.indent[c]]

                for l in range(0,number_l[0]):
                    
                    l_matrix = self.indent[c][m][l]*self.matrix[m*number_l[0]+l][0]
                    
                    if float(l % 2) != float(0):
                        l_matrix = l_matrix*-1
                        
                    matrix_l.append(l_matrix)
                
                
                matrix_i.append([])
                matrix_i[m].append(sum(matrix_l))
                
            self.matrix = matrix_i
                
        self.matrix = self.matrix[0][0]
        print(self.matrix)
        

    


        
        
        
    