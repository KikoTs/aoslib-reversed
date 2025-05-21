from aoslib cimport vxl
from shared cimport glm
cdef extern from "math.h":
    double floor(double x)

def cast_ray(vxl.VXL map, glm.Vector3 pos, glm.Vector3 dir, double length=32, bint isdirection=True):
    cdef long x, y, z
    if c_cast_ray(map.map_data, 
                 pos.cpp_obj.x, pos.cpp_obj.y, pos.cpp_obj.z,
                 dir.cpp_obj.x, dir.cpp_obj.y, dir.cpp_obj.z,
                 &x, &y, &z, length, isdirection):
        return x, y, z
    else:
        return False


cdef class WorldObject:
    def __init__(self, vxl.VXL map, *arg, **kwargs):
        self.map = map

    cdef long update(self, double dt, double time):
        return 0


cdef class Player:
    def __cinit__(self, vxl.VXL map):
        self.ply = new AcePlayer(map.map_data)
        self.position = glm.Vector3(self.ply.p_x, self.ply.p_y, self.ply.p_z)
        self.velocity = glm.Vector3(self.ply.v_x, self.ply.v_y, self.ply.v_z)
        self.orientation = glm.Vector3(self.ply.f_x, self.ply.f_y, self.ply.f_z)
        self.eye = glm.Vector3(self.ply.e_x, self.ply.e_y, self.ply.e_z)

    def __init__(self, vxl.VXL map):
        pass

    def __dealloc__(self):
        del self.ply
        
    cdef _sync_from_cpp(self):
        self.position.set(self.ply.p_x, self.ply.p_y, self.ply.p_z)
        self.velocity.set(self.ply.v_x, self.ply.v_y, self.ply.v_z)
        self.orientation.set(self.ply.f_x, self.ply.f_y, self.ply.f_z)
        self.eye.set(self.ply.e_x, self.ply.e_y, self.ply.e_z)
        
    cdef _sync_to_cpp(self):
        self.ply.p_x = self.position.cpp_obj.x
        self.ply.p_y = self.position.cpp_obj.y
        self.ply.p_z = self.position.cpp_obj.z
        self.ply.v_x = self.velocity.cpp_obj.x
        self.ply.v_y = self.velocity.cpp_obj.y
        self.ply.v_z = self.velocity.cpp_obj.z
        self.ply.f_x = self.orientation.cpp_obj.x
        self.ply.f_y = self.orientation.cpp_obj.y
        self.ply.f_z = self.orientation.cpp_obj.z
        self.ply.e_x = self.eye.cpp_obj.x
        self.ply.e_y = self.eye.cpp_obj.y
        self.ply.e_z = self.eye.cpp_obj.z

    def set_crouch(self, bint value):
        if value == self.ply.crouch:
            return
        if value:
            self.ply.p_z += 0.9
        else:
            self.ply.p_z -= 0.9
        self.ply.crouch = value
        self._sync_from_cpp()

    def set_animation(self, bint jump, bint crouch, bint sneak, bint sprint):
        if self.ply.airborne:
            jump = False
        self.ply.jump = jump
        self.set_crouch(crouch)
        self.ply.sneak = sneak
        self.ply.sprint = sprint

    def set_weapon(self, bint is_primary):
        self.ply.weapon = is_primary

    def set_walk(self, bint up, bint down, bint left, bint right):
        self.ply.mf = up
        self.ply.mb = down
        self.ply.ml = left
        self.ply.mr = right

    def set_fire(self, bint primary, bint secondary):
        self.ply.primary_fire = primary
        self.ply.secondary_fire = secondary

    def set_position(self, double x, double y, double z, bint reset=False):
        self.position.set(x, y, z)
        self.eye.set(x, y, z)
        self._sync_to_cpp()
        
        if reset:
            self.velocity.set(0, 0, 0)
            self._sync_to_cpp()
            self.set_walk(False, False, False, False)
            self.set_animation(False, False, False, False)
            self.set_fire(False, False)
            self.set_weapon(True)

    def set_dead(self, bint dead):
        self.ply.alive = not dead

    @property
    def mf(self):
        return self.ply.mf
    @mf.setter
    def mf(self, value):
        self.ply.mf = value

    @property
    def mb(self):
        return self.ply.mb
    @mb.setter
    def mb(self, value):
        self.ply.mb = value

    @property
    def ml(self):
        return self.ply.ml
    @ml.setter
    def ml(self, value):
        self.ply.ml = value

    @property
    def mr(self):
        return self.ply.mr
    @mr.setter
    def mr(self, value):
        self.ply.mr = value

    @property
    def jump(self):
        return self.ply.jump
    @jump.setter
    def jump(self, value):
        self.ply.jump = value

    @property
    def crouch(self):
        return self.ply.crouch
    @crouch.setter
    def crouch(self, value):
        self.set_crouch(value)

    @property
    def sneak(self):
        return self.ply.sneak
    @sneak.setter
    def sneak(self, value):
        self.ply.sneak = value

    @property
    def sprint(self):
        return self.ply.sneak
    @sprint.setter
    def sprint(self, value):
        self.ply.sprint = value

    @property
    def airborne(self):
        return self.ply.airborne

    @property
    def wade(self):
        return self.ply.wade

    @property
    def dead(self):
        return not self.ply.alive
    @dead.setter
    def dead(self, bint val):
        self.ply.alive = not val

    def set_orientation(self, double x, double y, double z):
        self.ply.set_orientation(x, y, z)
        self._sync_from_cpp()

    def update(self, double dt, double time):
        result = self.ply.update(dt, time)
        self._sync_from_cpp()
        return result


cdef class Grenade:
    def __cinit__(self, vxl.VXL map, double px, double py, double pz, double vx, double vy, double vz):
        self.grenade = new AceGrenade(map.map_data, px, py, pz, vx, vy, vz)
        self.position = glm.Vector3(self.grenade.p_x, self.grenade.p_y, self.grenade.p_z)
        self.velocity = glm.Vector3(self.grenade.v_x, self.grenade.v_y, self.grenade.v_z)

    def __init__(self, vxl.VXL map, double px, double py, double pz, double vx, double vy, double vz):
        pass

    def __dealloc__(self):
        del self.grenade
        
    cdef _sync_from_cpp(self):
        self.position.set(self.grenade.p_x, self.grenade.p_y, self.grenade.p_z)
        self.velocity.set(self.grenade.v_x, self.grenade.v_y, self.grenade.v_z)
        
    cdef _sync_to_cpp(self):
        self.grenade.p_x = self.position.cpp_obj.x
        self.grenade.p_y = self.position.cpp_obj.y
        self.grenade.p_z = self.position.cpp_obj.z
        self.grenade.v_x = self.velocity.cpp_obj.x
        self.grenade.v_y = self.velocity.cpp_obj.y
        self.grenade.v_z = self.velocity.cpp_obj.z

    def update(self, double dt, double time):
        result = self.grenade.update(dt, time)
        self._sync_from_cpp()
        return result

    def next_collision(self, double dt, double max):
        cdef:
            double eta
            double px, py, pz
        collides = self.grenade.next_collision(dt, max, &eta, &px, &py, &pz)
        pos = glm.Vector3(px, py, pz)
        if collides:
            return eta, pos
        else:
            return False, pos


# A generic object with collision detection
cdef class GenericMovement:
    def __init__(self, vxl.VXL map, double x, double y, double z):
        self.map = map
        self.position = glm.Vector3(x, y, z)

    def update(self, double dt, double time):
        return clipbox(self.map.map_data, floor(self.position.cpp_obj.x), floor(self.position.cpp_obj.y), floor(self.position.cpp_obj.z))
