c     ------------------------------
c     card punch graphics
c     ------------------------------
c
      pi=3.1415926
      do 40 i=0,20
c
      a1=(i/20.0)*(2.0*pi)
      a1=cosf(a1)
      a1=intf(a1*9)
      j=a1
      if (j) 10,11,12
   10 i1=0
      i2=10**(10+j)
      go to 15
   11 i1=0
      i2=10**9
      go to 15
   12 i1=10**j   
      i2=10**9
      go to 15
   15 continue
c
      a1=100.0-(i-10.0)*(i-10.0)
      a1=sqrtf(a1)
      a1=intf(9.0-a1*1.8)
      j=a1
      if (j) 20,21,22
   20 i3=0
      i4=10**(10+j)
      go to 25
   21 i3=0
      i4=10**9
      go to 25
   22 i3=10**j   
      i4=10**9
      go to 25
   25 continue
c
   40 punch,i,i1,i2,i3,i4
c     pause
      end
