C     array test
      DIMENSION A(5),X(3,4)
      A(3)=12
      X(1,1)=1
      X(2,1)=2
      X(3,1)=3

      X(1,2)=4
      X(2,2)=5
      X(3,2)=6

      X(1,3)=7
      X(2,3)=8
      X(3,3)=9

      X(1,4)=10
      X(2,4)=11
      X(3,4)=12

      I=2
      J=4
      X(I,J)=22

      PRINT X(2,3)
      
      PRINT X(I,J-2)

      PRINT X(2,4) - X(2,1)
      
