#!/usr/bin/env python3
"""
This is a demo program showing the use of the DifferentialDrive class,
specifically it contains the code necessary to operate a robot with
a single joystick
"""

import wpilib
import wpilib.drive
import ctre
import networktables_project as nt

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """Robot initialization function"""

        # motor controllers for traction
        self.m_left_front = ctre.WPI_VictorSPX(22)
        self.m_right_front = ctre.WPI_VictorSPX(33)
        self.m_left_rear = ctre.WPI_VictorSPX(11)
        self.m_right_rear = ctre.WPI_VictorSPX(44)

        self.shooter = ctre.WPI_VictorSPX(9)
        self.track_ball = ctre.WPI_VictorSPX(8)
        self.ball_catcher = ctre.WPI_VictorSPX(55)

        self.m_left = wpilib.SpeedControllerGroup(self.m_left_front, self.m_left_rear)
        self.m_right = wpilib.SpeedControllerGroup(self.m_right_front, self.m_right_rear)
	
        # object that handles basic drive operations
        self.myRobot = wpilib.drive.DifferentialDrive(self.m_left, self.m_right)
        self.myRobot.setExpiration(0.1)

        # joystick 0
        self.stick = wpilib.Joystick(0)

        # init camera
        wpilib.CameraServer.launch('vision.py:main')

        # create timer
        self.timer = wpilib.Timer()

    def teleopInit(self):
    # Executed at the start of teleop mode
        self.myRobot.setSafetyEnabled(True)

    def autonomousInit(self):
    #This function is run once each time the robot enters autonomous mode.
        self.timer.reset()
        self.timer.start()
        self.myRobot.setSafetyEnabled(True)
        nt.sd.putNumber("velocidadeT",500)
        nt.sd.putNumber("velocidadeR",45)

    def autonomousPeriodic(self):
    
        robotX = nt.sd.getNumber("robotX", -1)
        radius = nt.sd.getNumber("radius", -1)
        velocidadeT = nt.sd.getNumber("velocidadeT", -1)
        velocidadeR = nt.sd.getNumber("velocidadeR", -1)

        self.track_ball.set(1)
        self.ball_catcher.set(1)
        
        LIMITE_DE_ROTACAO = 0.45

        z_rotation_value = 2 * robotX - 1
        z_rotation_value = z_rotation_value * 2
        z_rotation_value = min(z_rotation_value, LIMITE_DE_ROTACAO)
        z_rotation_value = max(z_rotation_value, -LIMITE_DE_ROTACAO)

        # velocidadeT = 0

        if radius == -1:
            self.timer.start()
            self.myRobot.arcadeDrive(0, -velocidadeR/100, True)
            # if self.timer.get() >= 0.5:
            #     self.myRobot.arcadeDrive(0, 0, True)
            # self.timer.reset()
        else:
            self.myRobot.arcadeDrive(-(velocidadeT/1000), z_rotation_value, True)

    def teleopPeriodic(self):
    #Runs the motors with tank steering
    # to invert the axis when robot turns back
        if self.stick.getRawButton(5) == True:
            '''
            if self.stick.getRawAxis(0) < 0:
                self.myRobot.arcadeDrive(
                    -self.stick.getRawAxis(1), self.stick.getRawAxis(0)*1.15, True
                )
            else:
                self.myRobot.arcadeDrive(
                    -self.stick.getRawAxis(1), self.stick.getRawAxis(0), True
                )
            '''
            self.myRobot.arcadeDrive(
                -self.stick.getRawAxis(1), self.stick.getRawAxis(0)*1.15, True
            )
            
        else:
            '''
            if self.stick.getRawAxis(0) < 0:
                self.myRobot.arcadeDrive(
                    self.stick.getRawAxis(1), self.stick.getRawAxis(0)*1.15, True
                )
            else:
                self.myRobot.arcadeDrive(
                    self.stick.getRawAxis(1), self.stick.getRawAxis(0), True
                )
            '''
            self.myRobot.arcadeDrive(
                self.stick.getRawAxis(1), self.stick.getRawAxis(0)*1.15, True
            )
	

        # potencia = 1.15

	#self.m_left_front.set(0.5)

	# quadrado - pegar e subir
	# x - chutar
	# r1 - descer
	# o - desprender a bola

if __name__ == "__main__":
    wpilib.run(MyRobot)
