# rocket-evolution
Try and land a rocket or let an evolution algorithm do it for you.

## how to use
1. Install pygame

   ```
   pip install pygame
   ```
   
2. Run main.py
3. Play the game or watch the evolution simulator!

## project history
### introduction:
I had been wanting to make a simple rocket simulation like this for a little while, but only recently got around to finishing it. Using previous pygame knowledge, it was not too difficult to get the single player mode to work. However, when it came to adding the learning aspect to the training mode, it was not as simple.

### evolution approach v1.0:
Originally, I had thought that an evolutionary algorithm would easily be able to tackle this problem. What I did not know at the time however, was that the fitness score given to each rocket in the generation was being calculated incorrectly, causing little-to-no progress even when the training session reached the 1000th generation.

### neural net training approach:
When little progress was made with this approach, I tried something similar to what is implemented in the pong repository. The rocket would watch how you play in single player mode and try and emulate your moves based on what position and speed it is going. However, I quickly realized that the user would have to play far to many games in order to notice any progress in the trainable rocket.

### q learning approach:
Finally, I tried a basic Q-Learning approach. The rocket would be given a reward if it did a certain action in a particular position that led it closer to the landing zone and decreased its speed. Likewise, the rocket would be given a punishment if an action did not benefit it in a certain position. The rocket was also given a varying epsilon value to allow it to explore early on, and each action would update a Q Table. However, I think one of the main problems with this was that the rocket had momentum, particularly in the horizontal direction. It's a little difficult to explain, but essentially actions committed by the rocket were sometimes not instantaneous (due to the momentum of the rocket) and therefore the Q Table was not always updated with the correct reward or punishment.

### evolution approach v2.0:
Eventually, I was able to see my simple mistake with the evolutionary algorithm (rather than giving the rocket a score on its current position, it was also based on its past position as well), and the rockets were making significant progress as the generations progressed.
#### One side note:
Unlike most evolutionary algorithms, a rocket with a high score is worse than a rocket with a low score. I kept it this way to illustrate with the numbers how successful a rocket is. The score is based on the rocket's position relative to the landing zone, and its velocity. Therefore a rocket that is close to the landing zone and has a small speed is more likely to land safely.






