\ Model pickup_stations
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
 
Subject To
 Numbers[0,0]: - Select[0] + Assign[0,0] <= 0
 Numbers[0,1]: - Select[1] + Assign[0,1] <= 0
 Numbers[0,2]: - Select[2] + Assign[0,2] <= 0
 Numbers[0,3]: - Select[3] + Assign[0,3] <= 0
 Numbers[0,4]: - Select[4] + Assign[0,4] <= 0
 Numbers[0,5]: - Select[5] + Assign[0,5] <= 0
 Numbers[0,6]: - Select[6] + Assign[0,6] <= 0
 Numbers[0,7]: - Select[7] + Assign[0,7] <= 0
 Numbers[0,8]: - Select[8] + Assign[0,8] <= 0
 Numbers[0,9]: - Select[9] + Assign[0,9] <= 0
 Numbers[0,10]: - Select[10] + Assign[0,10] <= 0
 Numbers[0,11]: - Select[11] + Assign[0,11] <= 0
 Numbers[0,12]: - Select[12] + Assign[0,12] <= 0
 Numbers[0,13]: - Select[13] + Assign[0,13] <= 0
 Numbers[0,14]: - Select[14] + Assign[0,14] <= 0
 Numbers[0,15]: - Select[15] + Assign[0,15] <= 0
 Numbers[1,0]: - Select[0] + Assign[1,0] <= 0
 Numbers[1,1]: - Select[1] + Assign[1,1] <= 0
 Numbers[1,2]: - Select[2] + Assign[1,2] <= 0
 Numbers[1,3]: - Select[3] + Assign[1,3] <= 0
 Numbers[1,4]: - Select[4] + Assign[1,4] <= 0
 Numbers[1,5]: - Select[5] + Assign[1,5] <= 0
 Numbers[1,6]: - Select[6] + Assign[1,6] <= 0
 Numbers[1,7]: - Select[7] + Assign[1,7] <= 0
 Numbers[1,8]: - Select[8] + Assign[1,8] <= 0
 Numbers[1,9]: - Select[9] + Assign[1,9] <= 0
 Numbers[1,10]: - Select[10] + Assign[1,10] <= 0
 Numbers[1,11]: - Select[11] + Assign[1,11] <= 0
 Numbers[1,12]: - Select[12] + Assign[1,12] <= 0
 Numbers[1,13]: - Select[13] + Assign[1,13] <= 0
 Numbers[1,14]: - Select[14] + Assign[1,14] <= 0
 Numbers[1,15]: - Select[15] + Assign[1,15] <= 0
 serveOnce[0]: Assign[0,0] + Assign[0,1] + Assign[0,2] + Assign[0,3]
   + Assign[0,4] + Assign[0,5] + Assign[0,6] + Assign[0,7] + Assign[0,8]
   + Assign[0,9] + Assign[0,10] + Assign[0,11] + Assign[0,12]
   + Assign[0,13] + Assign[0,14] + Assign[0,15] = 1
 serveOnce[1]: Assign[1,0] + Assign[1,1] + Assign[1,2] + Assign[1,3]
   + Assign[1,4] + Assign[1,5] + Assign[1,6] + Assign[1,7] + Assign[1,8]
   + Assign[1,9] + Assign[1,10] + Assign[1,11] + Assign[1,12]
   + Assign[1,13] + Assign[1,14] + Assign[1,15] = 1
Bounds
 Assign[0,0] <= 1
 Assign[0,1] <= 1
 Assign[0,2] <= 1
 Assign[0,3] <= 1
 Assign[0,4] <= 1
 Assign[0,5] <= 1
 Assign[0,6] <= 1
 Assign[0,7] <= 1
 Assign[0,8] <= 1
 Assign[0,9] <= 1
 Assign[0,10] <= 1
 Assign[0,11] <= 1
 Assign[0,12] <= 1
 Assign[0,13] <= 1
 Assign[0,14] <= 1
 Assign[0,15] <= 1
 Assign[1,0] <= 1
 Assign[1,1] <= 1
 Assign[1,2] <= 1
 Assign[1,3] <= 1
 Assign[1,4] <= 1
 Assign[1,5] <= 1
 Assign[1,6] <= 1
 Assign[1,7] <= 1
 Assign[1,8] <= 1
 Assign[1,9] <= 1
 Assign[1,10] <= 1
 Assign[1,11] <= 1
 Assign[1,12] <= 1
 Assign[1,13] <= 1
 Assign[1,14] <= 1
 Assign[1,15] <= 1
Binaries
 Select[0] Select[1] Select[2] Select[3] Select[4] Select[5] Select[6]
 Select[7] Select[8] Select[9] Select[10] Select[11] Select[12] Select[13]
 Select[14] Select[15]
End
