from random import randint
from PIL import Image, ImageDraw, ImageChops, ImageStat

POPULATION_SIZE = 10 # NUMBER OF INDIVIDUALS IN THE POPULATION
ITERATIONS = 100000 # NUMBER OF ITERATIONS
NUM_OF_MUTANTS = 5 # NUMBER OF PRODUCED MUTANTS FROM ONE INDIVIDUAL

# CALCULATES ROOT-MEAN-SQUARE DEVIATION
def fitness(input_image, candidate):
    diff = ImageChops.difference(input_image, candidate) # GETTING DIFFERENCE BETWEEN IMAGES
    root_mean_square = ImageStat.Stat(diff).rms # CALCULATING ROOT-MEAN-SQUARE OF THE DIFFERENCE
    return sum(root_mean_square)

# SELECT THE BEST ONES FROM THE POPULATION BASED ON FITNESS
def select(population):
    sorted_population = sorted(population, key = lambda x: x[0]) # SORTING BY FITNESS
    return sorted_population[:POPULATION_SIZE] # SELECTING FIRST ONES 

# MUTATE INDIVIDUAL FROM THE POPULATION
def mutate_individual(individual):
    new_individual = individual.copy() 
    draw = ImageDraw.Draw(new_individual)
    # CREATING RANDOM COORDINATES
    x1 = randint(0, individual.width)
    y1 = randint(0, individual.width)
    x2 = randint(0, individual.height)
    y2 = randint(0, individual.height)
    # CREATING RANDOM COLOR
    color = (randint(1, 255), randint(1, 255), randint(1, 255))
    # DRAWING A RECTANGLE ON THE IMAGE ON RANDOM POSITION WITH RANDOM COLOR
    draw.rectangle((x1,y1,x2,y2), color) 
    return new_individual

# MUTATE POPULATION
def mutate(input_image, population):
    new_population = []
    for i in range(len(population)):
        new_population.append(population[i]) # ADDING THE INITIAL INDIVIDUAL TO THE NEW POPULATION
        for _ in range(NUM_OF_MUTANTS):
            mutant = mutate_individual(population[i][1]) # PRODUCING MUTANT
            new_population.append([fitness(input_image, mutant), mutant]) # ADDING MUTANT TO THE NEW POPULATION
    return new_population

# EVOLUTIONARY ALGORITHM
def evolution(input_image):
    init_fit = fitness(input_image, Image.new(input_image.mode, input_image.size, 'black')) 
    # INITIAL POPULATION
    population = [ [init_fit, Image.new(input_image.mode, input_image.size, 'black')] for _ in range(POPULATION_SIZE) ]
    # START EVOLUTIONARY ALGORITHM
    for i in range(ITERATIONS):
        if (i % 500 == 0):
            print(f'iteration #{i}')
        population = mutate(input_image, population) # MUTATE POPULATION
        population = select(population) # SELECT THE BEST INDIVIDUALS FROM THE POPULATION
    return population[0][1] # RETURNING THE BEST INDIVIDUAL

def main():
    input_image = Image.open('chert.jpg') 
    output_image = evolution(input_image)
    output_image.save('chert2.jpg')

if __name__ == '__main__':
    main()