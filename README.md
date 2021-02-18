# Snake AI

An artificially intelligent player for Snake. The snake's brain is a neural network and is improved via the genetic algorithm.

Snake game was accomplished through Python and the library pygame.     

<img src="https://user-images.githubusercontent.com/72149054/108436436-b897c580-724b-11eb-9409-5d38dd7544f6.jpg" alt="Selection" width="400" height="250"> <img src="https://user-images.githubusercontent.com/72149054/108436754-512e4580-724c-11eb-9dee-f9f9ed1a7088.jpg" alt="Selection" width="400" height="250">

### Using GA in NN
Steps:
- Creating a snake game and deciding neural network arhitecture
- Creating an initial population
- Deciding the fitness function
- Play a game for each individual in the population and sort each individual in the population based on the fitness function score
- Select a few top individuals from the population and create the remaining population from these top selected individuals using Crossover and Mutation
- The new population is created (meaning the next generation)
- Go to step 4 and repeat until the stopping criteria are not satisfied

#### Files:
- food.py / segment.py / snake.py - contains logic of creating snake game using pygame
- params.py - contains parameters that are using in a fitness function
- game.py - play snake game using predicted direction from genetic algortihm (GA)
- ai_trainer.py - contains genetic algorithm functions like crossover, mutation etc 
- ai_model.py - contains model of neural network and functions for initializing neural network weights and netwok prediction

#### Explanation:
##### Creating neural network
Snakes brains are neural nets with 4 layers:  
- input layer - 7 nodes 
- first hidden layer - 7 nodes with ‘relu’
- second hidden layer - 14 nodes with ‘relu’
- output layer - 3 nodes with ‘softmax’

Inputs in neural network: 
- distance from the snake's head to the fruit
- current snake speed (direction)
- whether the left, right and top neighbor field is empty or not  

Neural network output:
- probability to move up
- probability to move left 
- probability to move right    

    <img src="https://user-images.githubusercontent.com/72149054/108434985-d7e12380-7248-11eb-9b73-634d89ab08b5.jpg" alt="Selection" width="400" height="200">

Snake will go in the direction that has the highest probability

##### Deciding the Fitness Function

Any fitness function can be used here, I've used the following fitness function: “On every grasp of food, I have given reward points and if it collides with the boundary or itself, I have awarded a penalty points“.

##### Selection, Crossover, and Mutation
- Selection: Now, according to fitness value, some best individuals will be selected from the population. They will be the parents of the next generation
- Crossover: To produce children for the next generation, the crossover is used. First, two individuals are randomly selected from the best, then I randomly choose some values from first and some from the second individual to produce new offspring. This process is repeated until the total population size is not achieved
- Mutation: Then, some variations are being added to the newly formed offspring. Here, for each child, I randomly selected weights and mutated them by adding some random value

<img src="https://user-images.githubusercontent.com/72149054/108434975-d283d900-7248-11eb-9292-13b01f70da67.jpg" alt="Selection" width="320" height="200"> <img src="https://user-images.githubusercontent.com/72149054/108434977-d3b50600-7248-11eb-9e52-ec83965daa26.jpg" alt="Selection" width="320" height="200"> <img src="https://user-images.githubusercontent.com/72149054/108434980-d4e63300-7248-11eb-9f5f-cfc5d041d857.jpg" alt="Selection" width="320" height="200">

With the help of fitness function, crossover and mutation, new population for the next generation is created. Now, next thing is to replace the previous population with this newly formed. 
Now we will repeat this process until our target for certain game score is not achieved. You can choose number of generations and population size.


