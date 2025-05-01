C     Over-indexing demo
C       (overindexing was removed in FORTRAN 77)
      DIMENSION A(3,3)
      A(2,2)=25
      PRINT A(2,2),A(5,1)
      
