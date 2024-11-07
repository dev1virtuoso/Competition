# VEX IQ 2024

## Robots
Ivy
- Ivy (Operational)
- ![Ivy](assets/ivy.jpeg)

Sophie
- Sophie (Retired)
- ![Sophie](assets/sophie.jpeg)

Winter
- Winter (Retired)
- ![Winter](assets/winter.jpeg)

aespa

- aespa (Under Construction)
- ![aespa(Under Construction)](assets/aespa-constructing-1.jpeg)
- aespa(Under Testing)
- ![aespa(Under Testing)](assets/aespa-testing-1.jpeg)


## Members
  - Carson Wu
  - Kenny Ho
  - Leon Yao
  - Louis Chow
  - Marcus Tong
  - Yoyo Fung
  - Yoyo He
  - Yoyo Wong
  
## Components and Sensors Overview for Advanced Robotic Systems

1. **Shoot Mechanism (Flywheel)**
   - **Description:** The shoot mechanism involves a sophisticated flywheel system meticulously engineered to propel projectiles with unparalleled precision and accuracy. It functions by rapidly spinning a wheel to launch game objects or projectiles swiftly and reliably to their intended targets.

2. **Intake System (Roller)**
   - **Description:** The intake system features a specialized roller mechanism designed to adeptly gather game objects or materials with efficiency and speed. Its primary function is to swiftly collect and position items within the designated area for subsequent transfer to the shooting platform.

3. **Left Wheel Assembly**
   - **Description:** The left wheel assembly is a critical component responsible for facilitating the movement and agile maneuvering of the robot. This component plays a pivotal role in ensuring the robot's smooth navigation and precise control during operation.

4. **Color Sensor**
   - **Description:** The color sensor is a sophisticated device engineered to detect and differentiate colors with exceptional accuracy. It plays a crucial role in object recognition by identifying specific colors, enabling the robot to make informed decisions based on color cues.

5. **Distance Intake Sensor**
   - **Description:** The distance intake sensor is a precision instrument utilized to measure distances accurately for effective control of object intake. It plays a vital role in detecting the presence of objects within the intake area, ensuring seamless transfer and preventing objects from reaching the shooting platform prematurely.

6. **Distance Shoot Sensor**
   - **Description:** The distance shoot sensor is a specialized sensor designed to optimize shooting accuracy by precisely measuring distances within the shooting platform. It ensures that the platform is primed and ready for shooting by detecting the presence or absence of projectiles, facilitating efficient and accurate shooting operations.

7. **Shoot Mechanism (Flywheel)**
   - **Description:** Another instance of the flywheel-based shoot mechanism utilizes dual rapidly spinning wheels to propel projectiles with controlled force and consistency. This configuration enhances the robot's shooting capabilities, allowing for rapid and precise launching of game objects.

8. **Front Distance Sensor**
   - **Description:** Positioned at the front, the front distance sensor accurately gauges distances to aid in obstacle avoidance and precise navigation. It plays a crucial role in detecting obstacles or objects in the robot's path, enabling effective maneuvering and navigation in dynamic environments.

9. **Right Wheel Assembly**
   - **Description:** The right wheel assembly complements the left wheel assembly, ensuring balanced movement and responsive steering for the robot. This component is essential for maintaining stability and agility during operation, contributing to the overall maneuverability and performance of the robot.

10. **Pneumatic System**
    - **Description:** The pneumatic system harnesses compressed air to power various mechanical operations, such as actuating arms or mechanisms on the robot. It facilitates the controlled movement of components, enabling precise adjustments and efficient utilization of mechanical resources for optimal performance.

11. **Slider Motor**
    - **Description:** The slider motor is a key component responsible for controlling a slider mechanism, enabling specific movements and adjustments as needed during robot operations. It provides the robot with the capability to perform precise translational movements for tasks requiring fine adjustments or positional changes.

12. **Bumper Sensor**
    - **Description:** The strategically positioned bumper sensor serves as a critical safety feature, detecting physical contact or impacts to prevent collisions and ensure safe interaction control. When triggered, this sensor activates the shoot mechanism, allowing the robot to respond swiftly and effectively to potential collisions with obstacles or other objects.

## Flowchart of Autopilot System

```mermaid
graph TD
    A(Start Game) --> B{Color Detection}
    B -- Target Color --> C{Collect Items}
    C -- Items to Collect --> D{Navigate to Shooting Platform}
    D --> E{Prepare for Shooting}
    E -- Color Conflict --> F{Use Alternate Color}
    F --> G{Activate Shooting Mechanism}
    G --> H{Check Portal}
    H --> I{Check Game Progress}

    I -- Fire First Ball --> J{Collect Items}
    J --> K{Raise Shooting Platform}
    K --> L{Fire Second Ball}
    L --> M{Collect Items}
    M --> N{Move Left 60mm}
    N --> O{Fire Third Ball}
    O --> P{Collect Items}
    P --> Q{Lower Shooting Platform}
    Q --> R{Collect Items}
    R --> S{Game Over}

    B -- Different Color --> B
    C -- No Collection Needed --> D
    E -- No Color Conflict --> G
    F -- No Color Conflict Detected --> G
    I -- First Ball Not Fired --> I
    I -- First Ball Fired --> T{Additional Items to Collect?}
    
    T -- Items to Collect --> J
    T -- No Additional Items --> U{Adjust Shooting Platform Height?}

    U -- Adjust Needed --> K
    U -- No Adjustment Needed --> V{Need to Move Left?}
    
    V -- Move Left Needed --> N
    V -- No Move Left Needed --> W{Need to Lower Platform?}
    
    W -- Lower Platform Needed --> Q
    W -- No Lower Platform Needed --> X{Game Over?}

    X -- Game Not Over --> I
    X -- Game Over --> S{Stop Operation}

    S --> Y{Determine Score and Performance Metrics}
    I -- Ball Not Found --> Z{Rotate 360 degrees until Ball Found}
    Z --> I