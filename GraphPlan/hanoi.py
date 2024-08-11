import sys

def parse_vehicle_list(vehicle_list)
    # parse vehicle list from problem file
    # update main_vehicle, horizontal_vehicles and vertical_vehicles

    main_vehicle = [] # (left(x,y), right(x,y))
    horizontal_vehicles = [] # (name, left(x,y), right(x,y)) name = h0
    vertical_vehicles = [] # (name, top(x,y), bottom(x,y)) name = v0

    #TODO
    return main_vehicle, horizontal_vehicles, vertical_vehicles

def create_propositions()

    propositions = []

    # empty squares, filled squares propositions
    for x in range(width):
        for y in range(height):
            propositions.append(f'{x}_{y}_filled') #TODO not sure if we need this
            propositions.append(f'{x}_{y}_empty')

    # horizontal vehicles propositions
    for (car, (leftX, leftY), (rightX, rightY)) in self.horizontal_vehicles:
        propositions.append(f'{car}_left_{leftX}_{leftY}')
        propositions.append(f'{car}_right_{rightX}_{rightY}')

    # vertical vehicles propositions
    for (car, (topX, topY), (bottomX, bottomY)) in self.vertical_vehicles:
        propositions.append(f'{car}_top_{topX}_{topY}')
        propositions.append(f'{car}_bottom_{bottomX}_{bottomY}')
    
    # main_vehicle propositions
    propositions.append(f'main_left_{self.main_vehicle[0][0]}_{self.main_vehicle[0][1]}')
    propositions.append(f'main_right_{self.main_vehicle[1][0]}_{self.main_vehicle[1][1]}')

    return propositions

def create_actions()
    actions = []

    #TODO

    return actions

def create_domain_file(domain_file_name, height, width, vehicle_list):
    # this function should receive a list of vehicles and their orientation (horizontal, vertical) and their start and end positions, 
    # along with the width and height of the puzle
    # disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    # pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file
    # "*** YOUR CODE HERE ***"

    # main_vehicle = [] # (left(x,y), right(x,y))
    # horizontal_vehicles = [] # (name, left(x,y), right(x,y)) name = h0
    # vertical_vehicles = [] # (name, top(x,y), bottom(x,y)) name = v0

    main_vehicle, horizontal_vehicles, vertical_vehilces = parse_vehicle_list(vehicle_list)

    domain_file.write('Propositions:\n' + ' '.join(create_propositions()))

    domain_file.write('Actions:\n' + ' '.join(create_actions()))

    domain_file.close()



# def create_problem_file(problem_file_name_, n_, m_):
#     disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
#     pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
#     problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file
#     "*** YOUR CODE HERE ***"

#     problem_file.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: hanoi.py n m')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    m = int(float(sys.argv[2]))  # number of pegs

    domain_file_name = 'hanoi_%s_%s_domain.txt' % (n, m)
    problem_file_name = 'hanoi_%s_%s_problem.txt' % (n, m)

    create_domain_file(domain_file_name, n, m)
    create_problem_file(problem_file_name, n, m)
