#from django.test import TestCase
from unittest import TestCase

__author__ = 'himanshu'

#from osf.models import Timeline,History

import requests
import urllib
import datetime
import time
from datetime import tzinfo
import calendar


from endpoint_requests import *
#create_project,get_project,update_project,delete_project, delete_all_projects_in_range, delete_all_projects, determine_avg_time


class TestTimeline():
    def __init__(self):
        #d=convert_utc_format("09", "20","2014")
        self.original = {"title": 't1',
                             "author": 'a1',
                             #"date": str(d),
                             "wiki":'w1'}
        self.ports = [8000, 9000]
        #8000 is mongo
        #9000 is postgres
        #2424 is hybrid

    def works(self, should_be, actually_is, test_name):
        if should_be != actually_is:
            print test_name,"failed. It should have been:" ,should_be,"but was:",actually_is
            return False
        return True

    def test_simple(self):
        for p in self.ports:


            original = self.original.copy()
            t1 = time.time()
            original['project_id'] = 3000
            old = original.copy()

            x= create_project(3000,'09-20-2014', 't1','w1','a1', port=p)

            if not self.works(test_name="test_simple", should_be={3000:"Project Created."}, actually_is=x):
                return




            original['title']='t2'

            y= update_project(3000, date="09-21-2014", title= "t2", port=p)

            if not self.works(test_name="test_simple", should_be={3000: "Project Updated."}, actually_is=y):
                return
            z = get_project(3000, port=p)


            if not self.works(test_name="test_simple", should_be=original, actually_is=z):
                return

            q = get_project(3000,date="09-20-2014", port=p)

            if not self.works(test_name="test_simple", should_be=old, actually_is=q):
                return

            t2 = time.time()
            delete_all_projects(p)
            print "Port",p,": Went through all steps once for one project in",determine_avg_time([t2-t1], 1),"seconds"

    def test_view_current_x_times_with_y_updates(self, num_times, num_updates ):
        for p in self.ports:
            list_of_times=[]

            #initialize project creation
            x = create_project(1,'09-20-2014', 't1','w1','a1', port=p)
            if not self.works(test_name="test_view_current_x_times_with_y_updates", should_be={1:"Project Created."}, actually_is=x):
                return
            original = self.original.copy()
            original['project_id']=1

            #initialize updates
            for i in range(1,num_updates):
                y = update_project(1, date="09-20-"+str(2014+i), title='t'+str(1+i), port=p)
                if not self.works(test_name='test_view_current_x_times_with_y_updates', should_be={1:"Project Updated."}, actually_is=y):
                    return

            original['title'] = "t"+str(num_updates)
            #actual test
            for i in range(0,num_times):
                t1=time.time()

                #main test here.
                z = get_project(project_id=1, port=p)
                if not self.works(test_name='test_view_current_x_times_with_y_updates', should_be=original, actually_is=z):
                    return

                t2=time.time()
                list_of_times.append(t2-t1)


            print "Port",p, ": Ran",num_times,"views of project with", num_updates,"updates in average of ", determine_avg_time(list_of_times, num_times),"seconds"
            delete_all_projects(port=p)






    def test_simple_x_times(self, num_times):
        for p in self.ports:
            list_of_times = []

            for i in range(1,num_times+1):
                #clean
                t1 = time.time()
                original = self.original.copy()

                original['project_id'] = i
                old = original.copy()

                x = create_project(i,'09-20-2014', 't1','w1','a1', port=p)
                if not self.works(test_name="test_simple_x_times", should_be={i:"Project Created."}, actually_is=x):
                    return

                original['title']='t2'

                y = update_project(i, date="09-21-2014", title="t2", port=p)
                if not self.works(test_name="test_simple_x_times", should_be={i:"Project Updated."}, actually_is=y):
                    return

                z = get_project(i, port=p)
                if not self.works(test_name="test_simple_x_times", should_be=original, actually_is=z):
                    return


                q = get_project(i,date="09-20-2014", port=p)
                if not self.works(test_name="test_simple_x_times", should_be=old, actually_is=q):
                    return

                t2 = time.time()
                list_of_times.append(t2-t1)
            print "Port",p, ": Ran",num_times,"project iterations in average of ", determine_avg_time(list_of_times, num_times),"seconds"

            delete_all_projects(p)



    def test_x_updates(self, num_times):

        for p in self.ports:

            original = self.original.copy()
            original['project_id'] = 1
            old = original.copy()
            x = create_project(1,'09-20-2014', 't1','w1','a1', port=p)
            if not self.works(test_name="test_x_updates", should_be={1:"Project Created."}, actually_is=x):
                return

            list_of_times = []

            for i in range(2,num_times+2):
                t1 = time.time()

                y = update_project(1, date="09-21-"+str(2014+i), title='t'+str(i), port=p)
                if not self.works(test_name="test_x_updates", should_be={1:"Project Updated."}, actually_is=y):
                    return

                t2 = time.time()
                list_of_times.append(t2-t1)
            q = get_project(1, port=p)
            original['title']='t'+str(num_times+2-1)
            if not self.works(test_name="test_x_updates", should_be=original, actually_is=q):
                return
            print "Port",p, ": Ran", num_times ,"updates on single project in average of ",determine_avg_time(list_of_times, num_times),"seconds"
            delete_all_projects(p)

    def delete_all_in_db(self):
        for p in self.ports:
            delete_all_projects(p)




    def test_create_x_times(self,num_times):
        for p in self.ports:

            list_of_times=[]
            for i in range(1,num_times):
                original = self.original.copy()
                original['project_id'] = i

                t1=time.time()
                x = create_project(i,'09-20-2014', 't1','w1','a1', port=p)
                if not self.works(test_name="create_x_times",should_be={i:"Project Created."}, actually_is=x):
                    return
                t2 = time.time()
                list_of_times.append(t2-t1)
            print "Port",p,": Ran", num_times ,"creations of projects in average of",determine_avg_time(list_of_times, num_times),"seconds"
            delete_all_projects(p)


    def test_historical_view_of_x_distance(self,distance, num_views):
        for p in self.ports:

            list_of_times=[]

            original = self.original.copy()
            original['project_id'] = 1
            x = create_project(1,'09-20-2014', 't1','w1','a1', port=p)
            if not self.works(test_name="create_x_times",should_be={1:"Project Created."}, actually_is=x):
                    return
            #update distance times
            for i in range(1,distance+1):
                y=update_project(project_id=1,date='09-20-'+str(2014+i), title='t'+str(1+i), wiki="w"+str(1+i), port=p)
                if not self.works(test_name="historical_view_of_x_d",should_be={1:"Project Updated."}, actually_is=y):
                    return


            original['title']='t'+str(distance+1)
            original['wiki']='w'+str(distance+1)

            #actual testing part
            for i in range(0, num_views):
                t1=time.time()
                a = get_project(project_id=1, port=p)
                if not self.works(test_name="historical_view_of_x_distance", should_be=original, actually_is=a):
                    return
                t2=time.time()
                list_of_times.append(t2-t1)

            print "Port",p,": Ran", num_views ,"views of project. Distance is",distance,"AVG time is",determine_avg_time(list_of_times, num_views),"seconds"
            delete_all_projects(p)

    def test_original_version_x_times_with_y_updates_of_project(self, num_updates,num_views):
        for p in self.ports:

            list_of_times=[]

            original = self.original.copy()
            original['project_id'] = 1
            x = create_project(1,'09-20-2014', 't1','w1','a1', port=p)
            if not self.works(test_name="create_x_times",should_be={1:"Project Created."}, actually_is=x):
                    return
            #update distance times
            for i in range(1,num_updates+1):
                y=update_project(project_id=1,date='09-20-'+str(2014+i), title='t'+str(1+i), wiki="w"+str(1+i), author="a"+str(1+i), port=p)
                if not self.works(test_name="historical_view_of_x_d",should_be={1:"Project Updated."}, actually_is=y):
                    return

             #actual testing part
            for i in range(0, num_views):
                t1=time.time()
                a = get_project(project_id=1,date="09-20-2014", port=p)
                if not self.works(test_name="historical_view_of_x_distance", should_be=original, actually_is=a):
                    return
                t2=time.time()
                list_of_times.append(t2-t1)
            print "Port",p,": Ran", num_views ,"views of project. Distance is",num_updates,"AVG time is",determine_avg_time(list_of_times, num_views),"seconds"
            delete_all_projects(p)


def show_options(options):
    for (k,v) in options.iteritems():
        print k,"-", v
    return ""




if __name__=="__main__":
    while True:

        print "Input Test Option (each option tests all three set ups):"
        options={}

        options[0]="Exit"
        options[1]="simple all steps"
        options[2] ="all steps x times"
        options[3] ="create project x times"
        options[4] ="x updates."
        options[5] ="time to find old value that is x spots away. determines avg time for y such views"
        options[6] ="view current project x times with update spread y histories apart"
        options[7] = "view original version x times of project that has y updates"
        options[99]="delete everything from both db's (done automatically)'"
        test = TestTimeline()


        def case1():
            test.test_simple()
        def case2():
            test.test_simple_x_times(int(input("x:")))
        def case3():
            test.test_create_x_times(int(input("x:")))
        def case4():
            test.test_x_updates(int(input("x:")))
        def case5():
            test.test_historical_view_of_x_distance(distance=int(input("x:")),num_views=int(input("y:")))
        def case6():
            test.test_view_current_x_times_with_y_updates(num_times=int(input("x:")), num_updates=int(input("y:")))
        def case7():
            test.test_original_version_x_times_with_y_updates_of_project(num_views=int(input("x:")), num_updates=int(input("y:")) )
        def case99():
            test.delete_all_in_db()



        cases = {
            1: case1,
            2: case2,
            3: case3,
            4: case4,
            5: case5,
            6: case6,
            7: case7,
            99:case99,
        }
        option = int(input(show_options(options)))

        if option==0:
            break
        else:
            cases[option]()






#things to test:
#1) diff ports
#2) tons of updates
#3) time for each specific portion: create, update, get, get_historical
#4) determine if tweaks make faster
#5) diff amounts of input sizes - does larger input size make slower?
#6) how does concurrancy effect this. do so for all of these.

