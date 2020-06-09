\ Model pickup_stations
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
 
Subject To
 serveOnce[0]: Assign[0] + Assign[1] + Assign[2] + Assign[3] + Assign[4]
   + Assign[5] + Assign[6] + Assign[7] + Assign[8] + Assign[9] + Assign[10]
   + Assign[11] + Assign[12] + Assign[13] + Assign[14] + Assign[15]
   + Assign[16] + Assign[17] + Assign[18] = 1
 serveOnce[1]: Assign[19] + Assign[20] + Assign[21] + Assign[22]
   + Assign[23] + Assign[24] + Assign[25] + Assign[26] + Assign[27]
   + Assign[28] + Assign[29] + Assign[30] + Assign[31] + Assign[32]
   + Assign[33] + Assign[34] + Assign[35] + Assign[36] + Assign[37] = 1
 serveOnce[2]: Assign[38] + Assign[39] + Assign[40] + Assign[41]
   + Assign[42] + Assign[43] + Assign[44] + Assign[45] + Assign[46]
   + Assign[47] + Assign[48] + Assign[49] + Assign[50] + Assign[51]
   + Assign[52] + Assign[53] + Assign[54] + Assign[55] + Assign[56] = 1
 serveOnce[3]: Assign[57] + Assign[58] + Assign[59] + Assign[60]
   + Assign[61] + Assign[62] + Assign[63] + Assign[64] + Assign[65]
   + Assign[66] + Assign[67] + Assign[68] + Assign[69] + Assign[70]
   + Assign[71] + Assign[72] + Assign[73] + Assign[74] + Assign[75] = 1
 distance_lim[0,0]: 14508.61812854691 Assign[0] <= 4000
 distance_lim[0,1]: 1820.02747232013 Assign[1] <= 4000
 distance_lim[0,2]: 2061.55281280883 Assign[2] <= 4000
 distance_lim[0,3]: 5771.698190307598 Assign[3] <= 4000
 distance_lim[0,4]: 9513.148795220222 Assign[4] <= 4000
 distance_lim[0,5]: 3691.20576505835 Assign[5] <= 4000
 distance_lim[0,6]: 3816.084380618437 Assign[6] <= 4000
 distance_lim[0,7]: 6604.922406811454 Assign[7] <= 4000
 distance_lim[0,8]: 7215.434844830906 Assign[8] <= 4000
 distance_lim[0,9]: 10040.5428140116 Assign[9] <= 4000
 distance_lim[0,10]: 7280.109889280519 Assign[10] <= 4000
 distance_lim[0,11]: 9058.835465996719 Assign[11] <= 4000
 distance_lim[0,12]: 11800.42372120595 Assign[12] <= 4000
 distance_lim[0,13]: 10891.51045539598 Assign[13] <= 4000
 distance_lim[0,14]: 10934.46386431452 Assign[14] <= 4000
 distance_lim[0,15]: 12191.18534023661 Assign[15] <= 4000
 distance_lim[0,16]: 14346.16673540357 Assign[16] <= 4000
 distance_lim[0,17]: 17946.09985484311 Assign[17] <= 4000
 distance_lim[0,18]: 14508.61812854691 Assign[18] <= 4000
 distance_lim[1,0]: 19366.53040686431 Assign[19] <= 4000
 distance_lim[1,1]: 12313.61035602475 Assign[20] <= 4000
 distance_lim[1,2]: 12502.49975004999 Assign[21] <= 4000
 distance_lim[1,3]: 13752.27253947507 Assign[22] <= 4000
 distance_lim[1,4]: 15813.36460086847 Assign[23] <= 4000
 distance_lim[1,5]: 8591.42013871979 Assign[24] <= 4000
 distance_lim[1,6]: 8860.022573334674 Assign[25] <= 4000
 distance_lim[1,7]: 10550.4739230046 Assign[26] <= 4000
 distance_lim[1,8]: 4911.720676097125 Assign[27] <= 4000
 distance_lim[1,9]: 13124.40474840669 Assign[28] <= 4000
 distance_lim[1,10]: 5367.727638395972 Assign[29] <= 4000
 distance_lim[1,11]: 7850.159234053791 Assign[30] <= 4000
 distance_lim[1,12]: 11070.79491274227 Assign[31] <= 4000
 distance_lim[1,13]: 1600.781059358212 Assign[32] <= 4000
 distance_lim[1,14]: 2692.582403567252 Assign[33] <= 4000
 distance_lim[1,15]: 6329.494450586082 Assign[34] <= 4000
 distance_lim[1,16]: 10049.87562112089 Assign[35] <= 4000
 distance_lim[1,17]: 18500 Assign[36] <= 4000
 distance_lim[1,18]: 19366.53040686431 Assign[37] <= 4000
 distance_lim[2,0]: 19366.53040686431 Assign[38] <= 4000
 distance_lim[2,1]: 12313.61035602475 Assign[39] <= 4000
 distance_lim[2,2]: 12502.49975004999 Assign[40] <= 4000
 distance_lim[2,3]: 13752.27253947507 Assign[41] <= 4000
 distance_lim[2,4]: 15813.36460086847 Assign[42] <= 4000
 distance_lim[2,5]: 8591.42013871979 Assign[43] <= 4000
 distance_lim[2,6]: 8860.022573334674 Assign[44] <= 4000
 distance_lim[2,7]: 10550.4739230046 Assign[45] <= 4000
 distance_lim[2,8]: 4911.720676097125 Assign[46] <= 4000
 distance_lim[2,9]: 13124.40474840669 Assign[47] <= 4000
 distance_lim[2,10]: 5367.727638395972 Assign[48] <= 4000
 distance_lim[2,11]: 7850.159234053791 Assign[49] <= 4000
 distance_lim[2,12]: 11070.79491274227 Assign[50] <= 4000
 distance_lim[2,13]: 1600.781059358212 Assign[51] <= 4000
 distance_lim[2,14]: 2692.582403567252 Assign[52] <= 4000
 distance_lim[2,15]: 6329.494450586082 Assign[53] <= 4000
 distance_lim[2,16]: 10049.87562112089 Assign[54] <= 4000
 distance_lim[2,17]: 18500 Assign[55] <= 4000
 distance_lim[2,18]: 19366.53040686431 Assign[56] <= 4000
 distance_lim[3,0]: 19366.53040686431 Assign[57] <= 4000
 distance_lim[3,1]: 12313.61035602475 Assign[58] <= 4000
 distance_lim[3,2]: 12502.49975004999 Assign[59] <= 4000
 distance_lim[3,3]: 13752.27253947507 Assign[60] <= 4000
 distance_lim[3,4]: 15813.36460086847 Assign[61] <= 4000
 distance_lim[3,5]: 8591.42013871979 Assign[62] <= 4000
 distance_lim[3,6]: 8860.022573334674 Assign[63] <= 4000
 distance_lim[3,7]: 10550.4739230046 Assign[64] <= 4000
 distance_lim[3,8]: 4911.720676097125 Assign[65] <= 4000
 distance_lim[3,9]: 13124.40474840669 Assign[66] <= 4000
 distance_lim[3,10]: 5367.727638395972 Assign[67] <= 4000
 distance_lim[3,11]: 7850.159234053791 Assign[68] <= 4000
 distance_lim[3,12]: 11070.79491274227 Assign[69] <= 4000
 distance_lim[3,13]: 1600.781059358212 Assign[70] <= 4000
 distance_lim[3,14]: 2692.582403567252 Assign[71] <= 4000
 distance_lim[3,15]: 6329.494450586082 Assign[72] <= 4000
 distance_lim[3,16]: 10049.87562112089 Assign[73] <= 4000
 distance_lim[3,17]: 18500 Assign[74] <= 4000
 distance_lim[3,18]: 19366.53040686431 Assign[75] <= 4000
Bounds
Binaries
 Assign[0] Assign[1] Assign[2] Assign[3] Assign[4] Assign[5] Assign[6]
 Assign[7] Assign[8] Assign[9] Assign[10] Assign[11] Assign[12] Assign[13]
 Assign[14] Assign[15] Assign[16] Assign[17] Assign[18] Assign[19]
 Assign[20] Assign[21] Assign[22] Assign[23] Assign[24] Assign[25]
 Assign[26] Assign[27] Assign[28] Assign[29] Assign[30] Assign[31]
 Assign[32] Assign[33] Assign[34] Assign[35] Assign[36] Assign[37]
 Assign[38] Assign[39] Assign[40] Assign[41] Assign[42] Assign[43]
 Assign[44] Assign[45] Assign[46] Assign[47] Assign[48] Assign[49]
 Assign[50] Assign[51] Assign[52] Assign[53] Assign[54] Assign[55]
 Assign[56] Assign[57] Assign[58] Assign[59] Assign[60] Assign[61]
 Assign[62] Assign[63] Assign[64] Assign[65] Assign[66] Assign[67]
 Assign[68] Assign[69] Assign[70] Assign[71] Assign[72] Assign[73]
 Assign[74] Assign[75]
End
