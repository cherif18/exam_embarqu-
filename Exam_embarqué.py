import datetime
import time
import threading
import random


################################################################################
#   Handle all connections and rights for the server
################################################################################
class my_task():
    name = None
    priority = -1
    period = -1
    execution_time = -1
    last_execution_time = None
    last_execution_time_p1 = 0
    last_execution_time_p2 = 0
    last_execution_time_m1 = 0
    last_execution_time_m2 = 0

    ############################################################################
    def __init__(self, name, priority, period, execution_time, last_execution):
        self.name = name
        self.priority = priority
        self.period = period
        self.execution_time = execution_time

    def sauvegarde(self):
        self.last_execution_time_p1 = self.execution_time
        self.last_execution_time_p2 = self.execution_time
        self.last_execution_time_m1 = self.execution_time
        self.last_execution_time_m2 = self.execution_time


    ############################################################################
    def run(self):
        global temps_ecoule
        global arret_system
        global tank
        global stock1
        global stock2


        # Update last_execution_time
        self.last_execution_time = datetime.datetime.now()
        
            
        if self.name == "Pump 1" and self.period % 5 != 0:
            return
        if self.name == "Pump 2" and self.period % 15 != 0:
            return
        if self.name == "Machine 1" and self.period % 5 != 0:
            return
        if self.name == "Machine 2" and self.period % 5 != 0:
            return

        if self.name == "Pump 1" and self.last_execution_time_p1 <= 0:
            self.execution_time = 2
        if self.name == "Pump 2" and self.last_execution_time_p2 <= 0:
            self.execution_time = 3
        if self.name == "Machine 1" and self.last_execution_time_m1 <= 0:
            self.execution_time = 5
        if self.name == "Machine 2" and self.last_execution_time_m2 <= 0:
            self.execution_time = 3
            
        print(self.name + " : Starting task (" + self.last_execution_time.strftime(
            "%H:%M:%S") + ") : execution time = " + str(self.execution_time))

        print("Temps écoulé : " + str(temps_ecoule) + "; Reservoire : " + str(tank) + "; Stock pneus : " + str(stock1) + "; Stock moteurs : " + str(stock2))
            

        while (1):

            if (self.name == "Pump 1" or self.name == "Pump 2") and tank == 50:
                print("Pompe bloquée car reservoire est plein")
                return
            elif (self.name == "Pump 1" and tank + 10 > 50) or (self.name == "Pump 2" and tank + 20 > 50) :
                print("Pompe bloquée car l'ajout d'huile impliquera un excés de stockage")
                return
                
                
            if self.name == "Machine 1" and tank >= 25:
                if stock1 // 4 >= stock2:
                    print("Machine 1 bloquée car la fabrication de moteur est prioritaire")
                    return
                    
                
            if self.name == "Machine 2" and tank >= 5:
                if stock1 // 4 < stock2:
                    print("Machine 2 bloquée car la fabrication de roues est prioritaire")
                    return

            self.execution_time -= 1
            
            temps_ecoule += 1
            
            time.sleep(1)

            if self.execution_time <= 0:
                if self.name == "Pump 1":
                    tank += 10
                    print("Pump 1 : Produce 10 oil")
                elif self.name == "Pump 2":
                    tank += 20
                    print("Pump 2 : Produce 20 Oil")
                elif self.name == "Machine 1":
                    tank -= 25
                    stock1 += 1
                    print("Machine 1 : Produce 1 wheel")
                elif self.name == "Machine 2":
                    tank -= 5
                    stock2 += 1
                    print("Machine 2 : Produce 1 motor")
                    
                print(self.name + " : Terminating normally (" + datetime.datetime.now().strftime("%H:%M:%S") + ")")
                self.sauvegarde()
                print("Temps écoulé : " + str(temps_ecoule) + "; Reservoire : " + str(tank) + "; Stock pneus : " + str(stock1) + "; Stock moteurs : " + str(stock2))
                return
            
            
            self.sauvegarde()


####################################################################################################
#
#
#
####################################################################################################
if __name__ == '__main__':
    # Init and instanciation of watchdog

    # global watchdog
    # watchdog = False
    temps_ecoule = 0
    tank = 0
    stock1 = 0
    stock2 = 0
    


    # my_watchdog = Watchdog(period=10)  # Watchdog 10 seconds
    # my_watchdog.start()

    last_execution = datetime.datetime.now()

    # Instanciation of task objects
    task_list = [
        my_task(name="Pump 1", priority=1, period=5, execution_time=2, last_execution=last_execution),
        my_task(name="Pump 2", priority=1, period=15, execution_time=3, last_execution=last_execution),
        my_task(name="Machine 1", priority=1, period=5, execution_time=5, last_execution=last_execution),
        my_task(name="Machine 2", priority=1, period=5, execution_time=3, last_execution=last_execution)
    ]

    # Global scheduling loop
    incrementation = 0
    while (temps_ecoule < 120):
        print()
        print()
        print("\nScheduler tick " + str(incrementation) + " : " + datetime.datetime.now().strftime("%H:%M:%S"))
        incrementation += 1

        # Reinit watchdog
        #watchdog = False
        #my_watchdog.current_cpt = 10

        for task_to_run in task_list:
            print("The current time is: "+str(temps_ecoule));
            print()
            # Reinit watchdog
            # watchdog = False
            # my_watchdog.current_cpt = 10

            task_to_run.run()
