C     computed GO TO
      K=3
1     GO TO (10,20,30),K
10    PRINT K
      STOP
20    PRINT K,K
      K=K-1
      GO TO 1
30    PRINT K,K,K
      K=K-1
      GO TO 1
      END
      
