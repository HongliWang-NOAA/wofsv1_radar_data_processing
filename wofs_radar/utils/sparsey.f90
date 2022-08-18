recursive subroutine unfold(grid, val, x, y, z, nx, ny)
    implicit none

    real, intent(in) :: val
    integer, intent(in) :: x, y, z, nx, ny
    real, intent(inout) :: grid(0:nx-1,0:ny-1)

    integer distToEdge
    
    distToEdge = ny - y - 1

    IF (z .gt. distToEdge) THEN
        grid(x,y:(ny - 1)) = val
        IF (x + 1 .lt. nx) THEN
            CALL unfold(grid, val, x + 1, 0, z - distToEdge, nx, ny)
        ENDIF
    ELSE
        grid(x,y:(y + z - 1)) = val
    ENDIF

end subroutine unfold

subroutine sparse_decompress(v, x, y, z, dim, nx, ny, missing, grid)
    implicit none

    real, intent(in) :: v(0:dim-1)
    integer, intent(in) :: x(0:dim-1), y(0:dim-1), z(0:dim-1)
    integer, intent(in) :: dim, nx, ny   
    real, intent(in) :: missing
    real, intent(out) :: grid(0:nx-1,0:ny-1)

    integer i
    logical, parameter :: debug = .false.

    IF (debug) THEN
        print *, " dim ", dim
        print *, " nx ", nx
        print *, " ny ", ny
        print *, " missing ", missing
        print *, " maxval x ", maxval(x)
        print *, " maxval y ", maxval(y)
        print *, " maxval z ", maxval(z)
    ENDIF
     
    grid(:,:)   = missing  

    DO i = 0, dim - 1
        CALL unfold(grid, v(i), x(i), y(i), z(i), nx, ny)
    ENDDO
end subroutine sparse_decompress