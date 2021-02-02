# Enemy Test
This was the code used to test an enemy's movement in my friend's game. You can control the player using the arrow keys. There is no collision or anything like that; it's just testing the movement.
## Brief Explanation
This enemy will rush the player until it is a certain distance away from the player(I will call this distance r), then start orbiting around the player. The circle has radius r to show where the enemy will start orbiting. I will be calling the circle "orbit". The enemy will start running away if it is too close to the player(within the circle). 
The enemy has 4 "movement phases", which I will be listing below.
## Phase 1: Orbit Phase
When the enemy is really close to the player(within r±0.5 units away from the circle), this phase will be initiated. This signifies that the enemy is currently orbitting, so it will continue on the orbit.
## Phase 2: Going into Orbit Phase
When the enemy is within a close vicinity to the player(within r±10 units away from the circle), this phase will be initiated. This signifies that the enemy is close to the orbit. This will cause the enemy to go to the closest point on the orbit. 
## Phase 3: Rush Phase
When the enemy is farther than r+10 units away from the player(so outside of the circle and not **Phase 1** or **Phase 2**), then this phase will be initiated. When in this phase, the enemy will start heading towards the player. 
## Phase 4: Run Phase
When the enemy is closer than r-10 units away from the player(so really close to the player within the orbit), then this phase will be initiated. When in this phase, the enemy will start running away from the player. 
# Dependencies Required
[Pynput 1.7.2](https://pynput.readthedocs.io/en/latest/)
