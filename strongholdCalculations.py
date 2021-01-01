import math
def findStronghold(mc_x1, mc_z1, mc_d1, mc_x2, mc_z2, mc_d2):
    #The following is in equation form, on a graph that looks like https://minecraft.gamepedia.com/File:Minecraft_axes.png
    #the mc vars are on that graph, but we are changing these values to more like a standard graph
    if mc_d1 >= -90 and mc_d1 < 0: # Quadrant IV
        angle_eq1 = -90 - mc_d1
    elif mc_d1 < -90 and mc_d1 > -180: # Quadrant I
        angle_eq1 = -90 - mc_d1
    elif mc_d1 == 0 or mc_d1 == 180: # edge case to avoid undefined tangent error; could use try-except but nahhh
        angle_eq1 = 89.99
    elif mc_d1 > 0 and mc_d1 <= 90: # Quadrant II
        angle_eq1 = 90 - mc_d1
    elif mc_d1 < 180 and mc_d1 > 90: # Quadrant III
        angle_eq1 = 90 - mc_d1
    else:
        print("I is confuzion");

    slope_eq1 = math.tan(angle_eq1*math.pi/180)
    xpoint_eq1 = mc_x1
    ypoint_eq1 = -mc_z1
    yintercept_eq1 = ypoint_eq1-xpoint_eq1*slope_eq1

    #eq 2
    if mc_d2 >= -90 and mc_d2 < 0: # Quadrant IV
        angle_eq2 = -90 - mc_d2
    elif mc_d2 < -90 and mc_d2 > -180: # Quadrant I
        angle_eq2 = -90 - mc_d2
    elif mc_d2 == 0 or mc_d2 == 180: # edge case to avoid undefined tangent error; could use try-except but nahhh
        angle_eq2 = 89.99
    elif mc_d2 > 0 and mc_d2 <= 90: # Quadrant II
        angle_eq2 = 90 - mc_d2
    elif mc_d2 < 180 and mc_d2 > 90: # Quadrant III
        angle_eq2 = 90 - mc_d2
    else:
        print("I is confuzion");

    slope_eq2 = math.tan(angle_eq2*math.pi/180)
    xpoint_eq2 = mc_x2
    ypoint_eq2 = -mc_z2
    yintercept_eq2 = ypoint_eq2-xpoint_eq2*slope_eq2

    stronghold_x = (yintercept_eq2-yintercept_eq1)/(slope_eq1-slope_eq2)
    stronghold_y = slope_eq1*stronghold_x+yintercept_eq1;
    #convert back to minecraft coords
    stronghold_mc_x = stronghold_x
    stronghold_mc_z = -stronghold_y
    return stronghold_mc_x, stronghold_mc_z
