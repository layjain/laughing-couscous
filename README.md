# laughing-couscous

Run ```$ python3 app.py```  on terminal and navigate to ```localhost:5000``` on incongnito window. Choose epsilon and hit 'Analyze', and wait to see the histogram.

TODO:
1. Implement Signup Using Google API
7. Routing {{source}} (**IMPORTANT)**

10. Train/test accuracy; Remove labels in DPML(DONE: what labels to put?(Vaik)); Multi-dimensional DPML(*IMPORTANT: code supports just 2 dims)(Vaik); Ask user for ratio-split (Lay, Kafle)*

13. Display Weights (Done from back-end) ---> "theta" (Kafle)
14. Code Download (Vaik)
15. Change URL for DPVisualisation (Lay)
17. Handling error so that it does not load forever (Lay ----> Kafle)
18. Password-Reset, sending email (Lay)
19. Split Ratio
20. MultiDimensional Vaik
21. 3 mechanisms: Generalize Logistic Regression  (Lay) (Does not have degree? ---> Vaik)
			    : Naive Bayes (Lay, Kafle --> parameters: epsilon, split_ratio) (DONE)
			    : K-means (Lay, Kafle --> parameters: epsilon, split_ratio, number_of_clusters) (DONE)

22. Bounds are computed from the data in Naive Bayes --> privacy leak --> Vaik?
23. nan in the data (Lay)
24. Median code (Lay)
25. Error (Lay)
26. Change File does not work dynamnically(Kafle?)
27. Allow fractional epsilon values (Kafle)
28. Can handle high less than low from frontend? (Prabhakar?)
29. Disallow: e=0,d=0 in Laplace, BoundedLaplace, gaussian, Staircase (Prabhakar)
30. Is gamma = 1 / (1 + np.exp(epsilon / 2)) in staircase? (Vaik)
31. Add weights to NaiveBayes and Kmeans
32. Prabhakar: Handle dictionaries, for example, in /process
33. Vaik: Replace=True in Median??