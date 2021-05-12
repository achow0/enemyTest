# Enemy Test
This was the code used to test an enemy's movement in my friend's game. You can control the player using the arrow keys. There is no collision or anything like that; it's just testing the movement.
## Brief Explanation
This enemy will rush the player until it is a certain distance away from the player(I will call this distance r), then start orbiting around the player. The circle has radius r to show where the enemy will start orbiting. I will be calling the circle "orbit". The enemy will start running away if it is too close to the player(within the circle).
The enemy has 4 "movement phases", which I will be listing below.
## Phase 1: Orbit Phase
When the enemy is close to the player(within r±speed units away from the circle, where speed is referring to the speed of the enemy), this phase will be initiated. This signifies that the enemy is currently orbitting or entering into the orbit. This will either move the enemy into the orbit, or make the enemy continue on the orbit. 
## Phase 2: Rush Phase
When the enemy is farther than r+speed units away from the player(so both far from the orbit and outside the orbit), then this phase will be initiated. When in this phase, the enemy will start heading towards the player. 
## Phase 3: Run Phase
When the enemy is closer than r-speed units away from the player(so really close to the player within the orbit), then this phase will be initiated. When in this phase, the enemy will start running away from the player. 
# Dependencies Required
[Pynput 1.7.2](https://pynput.readthedocs.io/en/latest/)
