from distances import Distances as dist
import copy
import config
import numpy as np
import random

'''
Pesquisa local de Prins2004
'''


class LocalSearch:
    '''
    Cada iteração varre todos os pares possíveis de nós distintos (u,v). Esses nós podem pertencer à mesma viagem ou a viagens diferentes
    e um deles pode ser o depósito. x e y são os sucessores de u e v em suas respectivas viagens.
    @param Where opcional, para indicar onde o método é chamado, opções: None default ou 'ls'
    @param nMovimentations, para indicar se serão utilizados todos os movimentos ou apenas alguns. Opções: 'all' default ou 'random'
    '''

    def LS(self, solution, nMovimentations='all', where=None):

        movimentation = [self.M1,self.M2,self.M3, self.M4,self.M5,self.M6,self.M7,self.M8,self.M9,self.M10]
        lenght = len(movimentation)
        prob = config.PROB_LS
        # embaralhar os movimentos
        if nMovimentations == 'random':
            p = np.random.randint(1, round(0.3*lenght))
            movimentation = np.random.choice(movimentation, p, replace=False)
        else:
            prob = config.PROB_LS_BEST
            movimentation = np.random.choice(
                movimentation, lenght, replace=False)

        bestSolution = None
        bestSolution = copy.deepcopy(solution)

        if (where == 'ls' and np.random.random() < prob) or where == None:
            # print("vai mudar")
            # print(bestSolution)
            # print(bestSolution.get_routes())
            for i, m in enumerate(movimentation):
                # print(m)
                # print(solution)
                # print(solution.get_routes())
                solution1 = None
                solution1 = m(bestSolution)
                # tour = solution.get_giantTour()
                # for i, c1 in enumerate(tour):
                #     for j, c2 in enumerate(tour):
                #         if i != j and c1 == c2:
                #             print("Elementos iguais na LS")
                #             exit(1)
                # print(m)
                # print(solution1)
                # print(solution1.get_routes())

                if solution1.get_cost() < bestSolution.get_cost():
                    bestSolution = copy.deepcopy(solution1)
                    # print("achou melhor")
                else:
                    # excluir rotas vazias
                    bestSolution.removeRoutesEmpty()
                    # print("bestSolution")
                    # print(bestSolution)
                    return bestSolution

            # excluir rotas vazias
            bestSolution.removeRoutesEmpty()
            # print("não achou melhor")
        return bestSolution

    '''
    Método aplica a regra: Se u for um nó cliente, remova u e insira-o após v
    '''

    def M1(self, solution):
        solution1 = None
        solution1 = copy.deepcopy(solution)
        # print(solution1.get_routes())
        for routeU in solution1.get_routes():
            for i, u in enumerate(routeU.get_tour()):
                costRouteU = routeU.costWithoutNode(i)
                for routeV in solution1.get_routes():
                    for j, v in enumerate(routeV.get_tour()):
                        if u != v:  # se eles são diferentes

                            indJ = j
                            # print(u)
                            # print(v)
                            if u in routeV.get_tour() and v in routeU.get_tour():  # pertencem a mesma rota
                                # print("mesma rota")
                                auxRouteU = copy.deepcopy(routeU)
                                auxRouteU.popCustomer(i)
                                auxRouteU.set_cost(
                                    costRouteU[1], costRouteU[2], costRouteU[3])
                                if j > i:
                                    indJ = j - 1
                                costRouteV = auxRouteU.costWithNode(u, indJ+1)
                                newCost = solution.get_cost() - routeU.get_totalCost() + \
                                    costRouteV[0]
                            else:
                                # print("rotas diferentes")
                                costRouteV = routeV.costWithNode(u, indJ+1)
                                newCost = solution.get_cost() - routeU.get_totalCost() - \
                                    routeV.get_totalCost() + \
                                    costRouteU[0] + costRouteV[0]

                            # melhora a solução:
                            if newCost < solution.get_cost():
                                # remove u
                                U = routeU.popCustomer(i)
                                # insere u após v
                                routeV.insertCustomer(U, indJ+1)
                                # atualizar custos das rotas
                                routeU.set_cost(
                                    costRouteU[1], costRouteU[2], costRouteU[3])
                                routeV.set_cost(
                                    costRouteV[1], costRouteV[2], costRouteV[3])
                                # atualizar giantTour
                                solution1.formGiantTour()
                                solution1.calculateCost()
                                # print("rotas")

                                return solution1

                    # caso v seja o depósito
                    if u in routeV.get_tour():  # pertencem a mesma rota
                        auxRoute = None
                        auxRouteU = copy.deepcopy(routeU)
                        auxRouteU.popCustomer(i)
                        auxRouteU.set_cost(
                            costRouteU[1], costRouteU[2], costRouteU[3])
                        costRouteV = auxRouteU.costWithNode(u, 0)
                        newCost = solution.get_cost() - routeU.get_totalCost() + \
                            costRouteV[0]
                    else:
                        costRouteV = routeV.costWithNode(u, 0)
                        newCost = solution.get_cost() - routeU.get_totalCost() - \
                            routeV.get_totalCost() + \
                            costRouteU[0] + costRouteV[0]
                    # melhora a solução:
                    if newCost < solution.get_cost():
                        # print("no depósito")
                        # remove u
                        U = routeU.popCustomer(i)
                        # insere u após v
                        routeV.insertCustomer(U, 0)
                        # atualizar custos das rotas
                        routeU.set_cost(
                            costRouteU[1], costRouteU[2], costRouteU[3])
                        routeV.set_cost(
                            costRouteV[1], costRouteV[2], costRouteV[3])
                        # atualizar giantTour
                        solution1.formGiantTour()
                        solution1.calculateCost()
                        return solution1

        return solution

    '''
    Método aplica a regra: Se u e x forem clientes, remova-os e insira (u,x) após v
    '''

    def M2(self, solution):
        return self.M2orM3(solution, "M2")

    '''
    Método aplica a regra: Se u e x forem clientes, remova-os e insira (x,u) após v
    '''

    def M3(self, solution):
        return self.M2orM3(solution, "M3")

    '''
    Método aplica a regra: type: M2 -> Se u e x forem clientes, remova-os e insira (u,x) após v
                           type: M3 -> Se u e x forem clientes, remova-os e insira (x,u) após v
    '''

    def M2orM3(self, solution, type):
        solution1 = copy.deepcopy(solution)
        # print(solution1)
        for routeU in solution1.get_routes():
            for i, u in enumerate(routeU.get_tour()):
                if i+1 < len(routeU.get_tour()):
                    costRouteU = routeU.costWithout2Nodes(i)
                    for routeV in solution1.get_routes():
                        for j, v in enumerate(routeV.get_tour()):
                            # se u e x são diferentes de v
                            if u != v and routeU.get_tour()[i+1] != v:
                                indJ = j
                                if routeU is routeV:  # se pertencem a mesma rota:
                                    if j > i:
                                        indJ = j - 2
                                    auxRouteU = copy.deepcopy(routeU)
                                    auxRouteU.popCustomer(i)
                                    auxRouteU.popCustomer(i)
                                    auxRouteU.set_cost(
                                        costRouteU[1], costRouteU[2], costRouteU[3])
                                    if type.upper() == "M2":
                                        costRouteV = auxRouteU.costWith2Nodes(
                                            u, routeU.get_tour()[i+1], indJ+1)
                                    elif type.upper() == "M3":
                                        costRouteV = auxRouteU.costWith2Nodes(
                                            routeU.get_tour()[i+1], u, indJ+1)
                                    else:
                                        print("ERROR - método incorreto")
                                        exit(1)
                                    newCost = solution.get_cost() - routeU.get_totalCost() + \
                                        costRouteV[0]
                                    del auxRouteU
                                else:
                                    if type.upper() == "M2":
                                        costRouteV = routeV.costWith2Nodes(
                                            u, routeU.get_tour()[i+1], indJ+1)
                                    elif type.upper() == "M3":
                                        costRouteV = routeV.costWith2Nodes(
                                            routeU.get_tour()[i+1], u, indJ+1)
                                    else:
                                        print("ERROR - método incorreto")
                                        exit(1)
                                    newCost = solution.get_cost() - routeU.get_totalCost() - \
                                        routeV.get_totalCost() + \
                                        costRouteU[0] + costRouteV[0]
                                # melhora a solução:
                                if newCost < solution.get_cost():
                                    # print(costRouteU)
                                    #print("u e v:")
                                    # print(u)
                                    # print(v)
                                    # remove u e x
                                    U = routeU.popCustomer(i)
                                    X = routeU.popCustomer(i)
                                    # os insere após v
                                    if type.upper() == "M2":
                                        routeV.insertCustomer(U, indJ+1)
                                        routeV.insertCustomer(X, indJ+2)
                                    else:
                                        routeV.insertCustomer(X, indJ+1)
                                        routeV.insertCustomer(U, indJ+2)
                                    # atualizar custos das rotas
                                    routeU.set_cost(
                                        costRouteU[1], costRouteU[2], costRouteU[3])
                                    routeV.set_cost(
                                        costRouteV[1], costRouteV[2], costRouteV[3])
                                    # atualizar giantTour
                                    solution1.formGiantTour()
                                    solution1.calculateCost()
                                    return solution1

                       # caso v seja o depósito
                        auxRouteU = copy.deepcopy(routeU)
                        if type.upper() == "M2":
                            # print(auxRouteU)
                            if u in routeV.get_tour():  # se pertencem a mesma rota:
                                auxRouteU.popCustomer(i)
                                auxRouteU.popCustomer(i)
                                auxRouteU.set_cost(
                                    costRouteU[1], costRouteU[2], costRouteU[3])
                                costRouteV = auxRouteU.costWith2Nodes(
                                    u, routeU.get_tour()[i+1], 0)
                                newCost = solution.get_cost() - routeU.get_totalCost() + \
                                    costRouteV[0]
                                del auxRouteU
                            else:
                                costRouteV = routeV.costWith2Nodes(
                                    u, routeU.get_tour()[i+1], 0)
                                newCost = solution.get_cost() - routeU.get_totalCost() - \
                                    routeV.get_totalCost() + \
                                    costRouteU[0] + costRouteV[0]
                        else:
                            if u in routeV.get_tour():  # se pertencem a mesma rota:
                                auxRouteU.popCustomer(i)
                                auxRouteU.popCustomer(i)
                                auxRouteU.set_cost(
                                    costRouteU[1], costRouteU[2], costRouteU[3])
                                costRouteV = auxRouteU.costWith2Nodes(
                                    routeU.get_tour()[i+1], u, 0)
                                newCost = solution.get_cost() - routeU.get_totalCost() + \
                                    costRouteV[0]
                                del auxRouteU
                            else:
                                costRouteV = routeV.costWith2Nodes(
                                    routeU.get_tour()[i+1], u, 0)
                                newCost = solution.get_cost() - routeU.get_totalCost() - \
                                    routeV.get_totalCost() + \
                                    costRouteU[0] + costRouteV[0]
                        # melhora a solução:
                        if newCost < solution.get_cost():
                            #print("u e v depósito:")
                            # print(u)

                            # remove u e x
                            U = routeU.popCustomer(i)
                            X = routeU.popCustomer(i)
                            # os insere após v
                            if type.upper() == "M2":
                                routeV.insertCustomer(U, 0)
                                routeV.insertCustomer(X, 1)
                            else:
                                routeV.insertCustomer(X, 0)
                                routeV.insertCustomer(U, 1)
                            # atualizar custos das rotas
                            routeU.set_cost(
                                costRouteU[1], costRouteU[2], costRouteU[3])
                            routeV.set_cost(
                                costRouteV[1], costRouteV[2], costRouteV[3])
                            # atualizar giantTour
                            solution1.formGiantTour()
                            solution1.calculateCost()

                            return solution1

        return solution

    '''
    Método aplica a regra: Se u e v forem clientes, troque u e v
    '''

    def M4(self, solution):
        return self.M4orM5orM6(solution, "M4")

    '''
    Método aplica a regra: Se u, x e v são clientes, troque (u,x) e v
    '''

    def M5(self, solution):
        return self.M4orM5orM6(solution, "M5")

    '''
    Método aplica a regra: Se u, x, v e y são clientes, troque (u,x) e (v,y)
    '''

    def M6(self, solution):
        return self.M4orM5orM6(solution, "M6")

    '''
    Método aplica a regra: type => M4 - Se u e v forem clientes, troque u e v
                           type => M5 - Se u, x e v são clientes, troque (u,x) e v
                           type => M6 - Se u, x, v e y são clientes, troque (u,x) e (v,y)
    '''

    def M4orM5orM6(self, solution, type):
        solution1 = copy.deepcopy(solution)
        newCost = solution1.get_cost()
        costRouteU = None
        costRouteV = None
        for ru, routeU in enumerate(solution1.get_routes()):
            for i, u in enumerate(routeU.get_tour()):
                for routeV in solution1.get_routes():
                    for j, v in enumerate(routeV.get_tour()):
                        if u != v:

                            # se eles são de rotas diferentes
                            if u not in routeV.get_tour():
                                # print("u e v rotas diferntes")
                                # print(u)
                                # print(v)
                                # verificar se há melhora na solução com o procedimento
                                if type.upper() == "M4":
                                    listIdOld = [i]
                                    listNew = [v]
                                    costRouteU = routeU.costShiftNodes(
                                        listIdOld, listNew, routeU)
                                    
                                    listIdOld = [j]
                                    listNew = [u]
                                    costRouteV = routeV.costShiftNodes(
                                        listIdOld, listNew, routeV)

                                    newCost = solution.get_cost() - routeU.get_totalCost() - \
                                        routeV.get_totalCost() + \
                                        costRouteU[0] + costRouteV[0]
                                elif type.upper() == "M5":
                                    if i+1 < len(routeU.get_tour()):
                                        listIdOld = [i, i+1]
                                        listNew = [v]
                                        costRouteU = routeU.costShiftNodes(
                                            listIdOld, listNew, routeU)
                                        
                                        listIdOld = [j]
                                        listNew = [u, routeU.get_tour()[i+1]]
                                        costRouteV = routeV.costShiftNodes(
                                            listIdOld, listNew, routeV)

                                        newCost = solution.get_cost() - routeU.get_totalCost() - \
                                            routeV.get_totalCost() + \
                                            costRouteU[0] + costRouteV[0]

                                elif type.upper() == "M6":
                                    if i+1 < len(routeU.get_tour()) and j+1 < len(routeV.get_tour()):
                                        # print("Não devia entrar aqui")
                                        listIdOld = [i, i+1]
                                        listNew = [v, routeV.get_tour()[j+1]]
                                        costRouteU = routeU.costShiftNodes(
                                            listIdOld, listNew, routeU)
                                        
                                        listIdOld = [j, j+1]
                                        listNew = [u, routeU.get_tour()[i+1]]
                                        costRouteV = routeV.costShiftNodes(
                                            listIdOld, listNew, routeV)

                                        newCost = solution.get_cost() - routeU.get_totalCost() - \
                                            routeV.get_totalCost() + \
                                            costRouteU[0] + costRouteV[0]
                                else:
                                    print("ERROR - método incorreto")
                                    exit(1)

                                # print(routeU)
                                # print(routeV)
                                # melhora a solução:
                                auxRouteU = copy.deepcopy(routeU)
                                auxRouteV = copy.deepcopy(routeV)
                                if newCost < solution.get_cost():
                                    if type.upper() == "M4":
                                        routeU.popCustomer(i)
                                        routeU.insertCustomer(v, i)
                                        routeV.popCustomer(j)
                                        routeV.insertCustomer(u, j)
                                        routeU.set_cost(
                                            costRouteU[1], costRouteU[2], costRouteU[3])
                                        routeV.set_cost(
                                            costRouteV[1], costRouteV[2], costRouteV[3])
                                    elif type.upper() == "M5":
                                        if i+1 < len(routeU.get_tour()):
                                            routeU.popCustomer(i)
                                            routeU.insertCustomer(v, i)
                                            routeU.popCustomer(i+1)
                                            routeV.popCustomer(j)
                                            routeV.insertCustomer(u, j)
                                            routeV.insertCustomer(
                                                auxRouteU.get_tour()[i+1], j+1)
                                            routeU.set_cost(
                                                costRouteU[1], costRouteU[2], costRouteU[3])
                                            routeV.set_cost(
                                                costRouteV[1], costRouteV[2], costRouteV[3])
                                    elif type.upper() == "M6":
                                        if i+1 < len(routeU.get_tour()) and j+1 < len(routeV.get_tour()):
                                            routeU.popCustomer(i)
                                            routeU.insertCustomer(v, i)
                                            routeU.popCustomer(i+1)
                                            routeU.insertCustomer(
                                                auxRouteV.get_tour()[j+1], i+1)
                                            routeV.popCustomer(j)
                                            routeV.insertCustomer(u, j)
                                            routeV.popCustomer(j+1)
                                            routeV.insertCustomer(
                                                auxRouteU.get_tour()[i+1], j+1)
                                            routeU.set_cost(
                                                costRouteU[1], costRouteU[2], costRouteU[3])
                                            routeV.set_cost(
                                                costRouteV[1], costRouteV[2], costRouteV[3])
                                        # print(routeU)
                                        # print(routeV)
                                    # atualizar custos

                                    # atualizar giantTour
                                    solution1.formGiantTour()
                                    solution1.calculateCost()
                                    # tour = solution1.get_giantTour()
                                    # for ii, c1 in enumerate(tour):
                                    #     for jj, c2 in enumerate(tour):
                                    #         if ii != jj and c1 == c2:
                                    #             # print(i)
                                    #             # print(j)
                                    #             print("Elementos iguais")
                                    #             print("sa")
                                    #             print(solution)
                                    #             print(solution.get_routes())
                                    #             print("solution1")
                                    #             print(solution1)
                                    #             print(solution1.get_routes())
                                    #             print(routeU)
                                    #             print(routeV)
                                    #             print(auxRouteU)
                                    #             print(auxRouteV)
                                    #             print(u)
                                    #             print(v)
                                    #             exit(1)
                                    # del auxRouteU
                                    # del auxRouteV
                                    return solution1

                            else:
                                # print("mesma rota")
                                # print(i)
                                # print(j)
                                if type.upper() == "M4":
                                    aux1 = [i]
                                    aux2 = [j]
                                    costRouteU = routeU.costShiftNodesSameRoute(
                                        aux1, aux2, routeU)
                                    newCost = solution1.get_cost() - routeU.get_totalCost() + \
                                        costRouteU[0]
                                # print(routeU.get_tour()[aux1[0]])
                                # print(aux2)
                                elif type.upper() == "M5":
                                    if i+1 < len(routeU.get_tour()) and routeU.get_tour()[i+1] != v:

                                        aux1 = [i, i+1]
                                        aux2 = [j]
                                        costRouteU = routeU.costShiftNodesSameRoute(
                                            aux1, aux2, routeU)
                                        newCost = solution1.get_cost() - routeU.get_totalCost() + \
                                            costRouteU[0]
                                elif type.upper() == "M6":
                                    maximum = max(i, j)
                                    minor = min(i, j)
                                    if maximum+1 < len(routeU.get_tour()) and minor+1 < maximum:
                                        # print("problema aqui")
                                        aux1 = [i, i+1]
                                        aux2 = [j, j+1]
                                        costRouteU = routeU.costShiftNodesSameRoute(
                                            aux1, aux2, routeU)
                                        newCost = solution1.get_cost() - routeU.get_totalCost() + \
                                            costRouteU[0]

                                # print(costRouteU)
                                # print(newCost)
                                # print(solution.get_cost())
                                # melhora a solução:
                                if newCost < solution1.get_cost():
                                    solution1.setRoute(costRouteU[1], ru)
                                    # print(routeU)
                                    # print(solution1)
                                    # atualizar giantTour
                                    solution1.formGiantTour()
                                    solution1.calculateCost()
                                    return solution1

        return solution

    '''
    Método aplica a regra: Se T(u) == T(v), substitua (u,x) e (v,y) por (u,v) e (x,y)
    '''

    def M7(self, solution):
        solution1 = copy.deepcopy(solution)
        for ru, routeU in enumerate(solution1.get_routes()):
            for i, u in enumerate(routeU.get_tour()):
                for routeV in solution1.get_routes():
                    for j, v in enumerate(routeV.get_tour()):
                        if u is not v:
                            # se eles são da mesma rota
                            if (u in routeV.get_tour()) and (v in routeU.get_tour()):
                                def minor(x, y): return x if x < y else y
                                def maximum(x, y): return x if x > y else y
                                max = maximum(i, j)
                                min = minor(i, j)
                                if max+1 < len(routeU.get_tour()) and min+1 < max:
                                    aux1 = [i, i+1]
                                    replaceWith1 = [u, v]
                                    # print("aux1")
                                    # print(aux1)
                                    # print("replaceWith1")
                                    # print(replaceWith1)
                                    aux2 = [j, j+1]
                                    replaceWith2 = [
                                        routeU.get_tour()[i+1], routeU.get_tour()[j+1]]
                                    # print("aux2")
                                    # print(aux2)
                                    # print("replaceWith2")
                                    # print(replaceWith2)
                                    costRouteU = routeU.costReplaceNodes(
                                        routeU, aux1, replaceWith1, aux2, replaceWith2)
                                    newCost = solution.get_cost() - routeU.get_totalCost() + \
                                        costRouteU[0]
                                    # print(costRouteU)
                                    # melhora a solução:
                                    if newCost < solution.get_cost():
                                        solution1.get_routes()[ru] = None
                                        solution1.get_routes()[
                                            ru] = costRouteU[1]
                                        # atualizar giantTour
                                        solution1.formGiantTour()
                                        solution1.calculateCost()
                                        return solution1

        return solution

    '''
    Método aplica a regra: Se T(u) != T(v), substitua (u,x) e (v,y) por (u,v) e (x,y)
    '''

    def M8(self, solution):
        return self.M8orM9(solution, "M8")

    '''
    Método aplica a regra: Se T(u) != T(v), substitua (u,x) e (v,y) por (u,y) e (x,v)
    '''

    def M9(self, solution):
        return self.M8orM9(solution, "M9")

    '''
    Método aplica a regra: type => M8 - Se T(u) != T(v), substitua (u,x) e (v,y) por (u,v) e (x,y)
                           type => M9 - Se T(u) != T(v), substitua (u,x) e (v,y) por (u,y) e (x,v)
    '''

    def M8orM9(self, solution, type):
        solution1 = copy.deepcopy(solution)
        for ru, routeU in enumerate(solution1.get_routes()):
            for i, u in enumerate(routeU.get_tour()):
                for rv, routeV in enumerate(solution1.get_routes()):
                    for j, v in enumerate(routeV.get_tour()):
                        if u != v:
                            # se eles não são da mesma rota
                            if (u not in routeV.get_tour()) and (v not in routeU.get_tour()):
                                if i+1 < len(routeU.get_tour()) and j+1 < len(routeV.get_tour()):
                                    if type.upper() == "M8":
                                        aux1 = [i, i+1]
                                        replaceWith1 = [u, v]
                                        aux2 = [j, j+1]
                                        replaceWith2 = [
                                            routeU.get_tour()[i+1], routeV.get_tour()[j+1]]
                                    elif type.upper() == "M9":
                                        aux1 = [i, i+1]
                                        replaceWith1 = [
                                            u, routeV.get_tour()[j+1]]
                                        aux2 = [j, j+1]
                                        replaceWith2 = [
                                            routeU.get_tour()[i+1], v]
                                    else:
                                        print("ERROR - método incorreto")
                                        exit(1)

                                    # mudança na rota U
                                    costRouteU = routeU.costReplaceNodes(
                                        routeU, aux1, replaceWith1)
                                    # print("aux1")
                                    # print(aux1)
                                    # print("replaceWith1")
                                    # print(replaceWith1)
                                    # mudança na rota V
                                    costRouteV = routeV.costReplaceNodes(
                                        routeV, aux2, replaceWith2)
                                    # print("aux2")
                                    # print(aux2)
                                    # print("replaceWith2")
                                    # print(replaceWith2)

                                    newCost = solution.get_cost() - routeU.get_totalCost() - \
                                        routeV.get_totalCost() + \
                                        costRouteU[0] + costRouteV[0]

                                    if newCost < solution.get_cost():
                                        solution1.get_routes()[ru] = None
                                        solution1.get_routes()[
                                            ru] = costRouteU[1]
                                        solution1.get_routes()[rv] = None
                                        solution1.get_routes()[
                                            rv] = costRouteV[1]
                                        # atualizar giantTour
                                        solution1.formGiantTour()
                                        solution1.calculateCost()
                                        return solution1

        return solution

    '''
    Rotation 
    Bolaños 2018
    Não verifica melhor depósito - por enquanto
    '''

    def M10(self, solution):
        solution1 = copy.deepcopy(solution)
        routes = solution1.get_routes()
        idRoute = np.random.randint(len(routes))
        route = copy.deepcopy(routes[idRoute])
        length = len(route.get_tour())
        betterRoute = copy.deepcopy(route)
        route1 = copy.deepcopy(route)
        # oldDepot = route1.get_depot()
        cont = 0
        # print("betterRoute")
        # print(betterRoute)
        for i in range(length-1):
            aux = route1.get_tour()[0]
            # print(aux)
            cost = route1.costWithoutNode(0)
            route1.removeCustomer(aux)
            route1.set_cost(cost[1], cost[2], cost[3])
            cost = route1.costWithNode(aux, length-1)
            route1.addCustomer(aux)
            route1.set_cost(cost[1], cost[2], cost[3])
            # print(route1)

            if betterRoute.get_totalCost() > route1.get_totalCost():
                # print("achou melhor")
                betterRoute = copy.deepcopy(route1)
                cont = 1
        if cont == 1:
            solution1.setRoute(betterRoute, idRoute)
            solution1.formGiantTour()
            solution1.calculateCost()
            return solution1

        return solution
