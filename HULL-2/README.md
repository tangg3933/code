# HULL-2
Up to 17/10/2021
Pervious implementation of calculation hull was wrong, it calculated convex hull, but part B requires concave hull. However, it can still be used as the input data for part C. Regardless of concave or convex, they are all data points, and part C is all about reducing data points.
Concave hull calculation is completed and validated, and part C is modified based on new part B's result. The result looks fine.
Planned to merge all parts of code later.


Up to 3/10/2021
Implemented HULL Aggregation using divide and conquer method, two py files have been uploaded into code, more detail, please refer to their code comments, both functions are based on 3D to 2D's result (examined)
please refer to:

HullAggregate_Single.py:
Mainly used for Valid previous implementation of 3D to 2D, by comparing open3D's API's result (based on 3D) and our implementation (2D based), the result is identical, which prove both 3D to 2D and hull aggregation were correct.

HullAggregate_Whole.py
After validation, now use multiple obj files as input.


Up to 8/9/2021
The 3Dto2D.py is to find a set of 2D projected points along z-axis for a single obj file. Further implementation about projections along different faces will be consider after next meeting. The class ReadData in classes directory is able to convert obj file information to two set of lists. One list is about vertices, the other is about faces.


Up to 5/9/2021
Some code was uploaded. Read-Object.py is an alternative way to display the 3d model, and it works on all platforms, so if any of you haven't compiled the vs project they provided, you can use this, just pip install open3d

Calculate-HULL.py is the combined part a and part b code, initial demo only, relying on 3rd party python library. The part A result should be correct, but not sure if part b meet their requirements or not. I already contacted the company side to examine this. Hopefully, we can get some feedback next week.

Meanwhile, everyone can now try these codes and provide their feedback during week 7's meeting.
For who is responsible for the C# wrapper, they can start now.


Up to 29/8/2021

We have "Coder" and "Researcher".
"Researcher" is responsible for studying the problem and providing initial solutions; they are expected to find online libraries or provide pseudocode and validate their solution before committing.
"Coder" will be responsible implement completed designed, examined solutions from the "Researcher". At this stage, the coder will provide study and write documentation that adapts this project.

Rules regarding documentation writing and few tips in studying have been provided. See HULL-2/Documentations/README.

Next:
All group members are supposed to participate in the Week 6 meeting with clients and the group meeting next week. The initial research should be completed and will select the most examinable solution to implement.
