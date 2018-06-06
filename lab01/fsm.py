# State Machine Spike 1

print ("starting state machine")

# Variables
energy = 35
bloodlust = 20
health = 5

states = ['moving', 'resting', 'fighting']
current_state = 'moving'

alive = True

while alive:
    
    # Moving: Increase Bloodlust, Reduce Energy
    if current_state is 'moving':
        print("Stomp, Stomp, Stomp")
        bloodlust += 2
        energy -= 5
        if energy < 30:
            current_state = 'resting'
        elif energy > 30 and bloodlust > 30:
            current_state = 'fighting'
        
    # Resting: Incrase Energy and Health, Reduce Bloodlust
    elif current_state is 'resting':
        print("ZZZZZ")
        bloodlust -= 1
        energy += 10
        if health < 5:
            health += 1
        if energy > 40 and bloodlust < 30:
            current_state = 'moving'
        elif energy > 40 and bloodlust > 30:
            current_state = 'fighting'
            
    # Fighting: Reduce Energy, Bloodlust and Health
    elif current_state is 'fighting':
        print("ugh, hya")
        bloodlust -= 1
        energy -= 10
        health -= 1
        if energy < 10:
            current_state = 'resting'
        elif energy > 10 and bloodlust < 10:
            current_state = 'moving'

    if energy < 1:
        health -= 3
    if health < 1:
        print ("aghhhhhhhhhhhh!!!!!!!!")
        alive = False
        

print ("<----The-End---->")

