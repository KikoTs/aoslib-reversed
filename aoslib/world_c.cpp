#include <cmath>

#include "vxl_c.h"
#include "../shared/glm_c.h"

constexpr float FALL_SLOW_DOWN = 0.24f;
constexpr float FALL_DAMAGE_VELOCITY = 0.58f;
constexpr int FALL_DAMAGE_SCALAR = 4096;

// Simple Vector3 struct for internal use
struct Vector {
    double x, y, z;
    
    Vector(double x=0, double y=0, double z=0) : x(x), y(y), z(z) {}
    
    void set(double nx, double ny, double nz) {
        x = nx;
        y = ny;
        z = nz;
    }
};

struct AcePlayer {
    explicit AcePlayer(AceMap *map) {
        this->map = map;
        this->mf = this->mb = this->ml = this->mr = false;
        this->jump = this->crouch = this->sneak = this->sprint = false;
        this->primary_fire = this->secondary_fire = this->weapon = false;
        this->airborne = this->wade = false;
        this->alive = true;
        this->lastclimb = 0.0;
        
        // Initialize vectors
        this->p_x = 0; this->p_y = 0; this->p_z = 0;
        this->v_x = 0; this->v_y = 0; this->v_z = 0;
        this->e_x = 0; this->e_y = 0; this->e_z = 0;
        this->f_x = 1; this->f_y = 0; this->f_z = 0;
        this->s_x = 0; this->s_y = 1; this->s_z = 0;
        this->h_x = 0; this->h_y = 0; this->h_z = 1;
    }
    long update(double dt, double time);
    void set_orientation(double x, double y, double z);

    AceMap *map;
    bool mf, mb, ml, mr, jump, crouch, sneak, sprint, primary_fire, secondary_fire, airborne, wade, alive, weapon;
    double lastclimb;
    
    // Position, eye position, velocity and orientation vectors as components
    double p_x, p_y, p_z;  // Position
    double e_x, e_y, e_z;  // Eye position
    double v_x, v_y, v_z;  // Velocity
    double f_x, f_y, f_z;  // Forward direction
    double s_x, s_y, s_z;  // Side direction
    double h_x, h_y, h_z;  // Up direction

private:
    void boxclipmove(double dt, double time);
    void reposition(double dt, double time);
    
    // Helper methods to work with old Vector-based code
    Vector getPosition() const { return Vector(p_x, p_y, p_z); }
    Vector getVelocity() const { return Vector(v_x, v_y, v_z); }
    Vector getForward() const { return Vector(f_x, f_y, f_z); }
    Vector getSide() const { return Vector(s_x, s_y, s_z); }
    
    void setPosition(const Vector& v) { p_x = v.x; p_y = v.y; p_z = v.z; }
    void setVelocity(const Vector& v) { v_x = v.x; v_y = v.y; v_z = v.z; }
    void setForward(const Vector& v) { f_x = v.x; f_y = v.y; f_z = v.z; }
    void setSide(const Vector& v) { s_x = v.x; s_y = v.y; s_z = v.z; }
    void setUp(const Vector& v) { h_x = v.x; h_y = v.y; h_z = v.z; }
};

struct AceGrenade {
    AceGrenade(AceMap *map, double px, double py, double pz, double vx, double vy, double vz) : map(map) {
        p_x = px; p_y = py; p_z = pz;
        v_x = vx; v_y = vy; v_z = vz;
    }
    bool update(double dt, double time);
    bool next_collision(double dt, double max, double *eta, double *px, double *py, double *pz);

    AceMap *map;
    double p_x, p_y, p_z;  // Position
    double v_x, v_y, v_z;  // Velocity
    
    // Helper methods to work with old Vector-based code
    Vector getPosition() const { return Vector(p_x, p_y, p_z); }
    Vector getVelocity() const { return Vector(v_x, v_y, v_z); }
    
    void setPosition(const Vector& v) { p_x = v.x; p_y = v.y; p_z = v.z; }
    void setVelocity(const Vector& v) { v_x = v.x; v_y = v.y; v_z = v.z; }
};

// should these be methods on AceMap ?
//same as isvoxelsolid but water is empty && out of bounds returns true
bool clipbox(AceMap *map, float x, float y, float z)
{
    if (x < 0 || x >= MAP_X || y < 0 || y >= MAP_Y)
        return true;
    if (z < 0)
        return false;

    int sz = z;
    if (sz == MAP_Z - 1)
        sz -= 1;
    else if (sz >= MAP_Z)
        return true;
    return map->get_solid(x, y, sz);
}

//same as isvoxelsolid but water is empty
bool clipworld(AceMap *map, long x, long y, long z)
{
    if (x < 0 || x >= MAP_X || y < 0 || y >= MAP_Y)
        return false;
    if (z < 0)
        return false;

    int sz = z;
    if (sz == 63)
        sz = 62;
    else if (sz >= 63)
        return true;
    else if (sz < 0)
        return false;
    return map->get_solid(x, y, sz);
}

long AcePlayer::update(double dt, double time) {
    //move player and perform simple physics (gravity, momentum, friction)
    if (this->jump)
    {
        this->jump = false;
        this->v_z = -0.36f;
    }

    float f = dt; //player acceleration scalar
    if (this->airborne)
        f *= 0.1f;
    else if (this->crouch)
        f *= 0.3f;
    else if ((this->secondary_fire && this->weapon) || this->sneak)
        f *= 0.5f;
    else if (this->sprint)
        f *= 1.3f;

    if ((this->mf || this->mb) && (this->ml || this->mr))
        f *= sqrt(0.5); //if strafe + forward/backwards then limit diagonal velocity

    if (this->mf)
    {
        this->v_x += this->f_x*f;
        this->v_y += this->f_y*f;
    }
    else if (this->mb)
    {
        this->v_x -= this->f_x*f;
        this->v_y -= this->f_y*f;
    }
    if (this->ml)
    {
        this->v_x -= this->s_x*f;
        this->v_y -= this->s_y*f;
    }
    else if (this->mr)
    {
        this->v_x += this->s_x*f;
        this->v_y += this->s_y*f;
    }

    f = dt + 1;
    this->v_z += dt;
    this->v_z /= f; //air friction
    if (this->wade)
        f = dt*6.f + 1; //water friction
    else if (!this->airborne)
        f = dt*4.f + 1; //ground friction
    this->v_x /= f;
    this->v_y /= f;
    float f2 = this->v_z;
    this->boxclipmove(dt, time);
    //hit ground... check if hurt
    if (!this->v_z && (f2 > FALL_SLOW_DOWN))
    {
        //slow down on landing
        this->v_x *= 0.5f;
        this->v_y *= 0.5f;

        //return fall damage
        if (f2 > FALL_DAMAGE_VELOCITY)
        {
            f2 -= FALL_DAMAGE_VELOCITY;
            return f2 * f2 * FALL_DAMAGE_SCALAR;
        }

        return -1; // no fall damage but play fall sound
    }

    return 0; //no fall damage
}

void AcePlayer::set_orientation(double x, double y, double z) {
    float f = sqrtf(x*x + y*y);
    this->f_x = x;
    this->f_y = y;
    this->f_z = z;
    
    this->s_x = -y / f;
    this->s_y = x / f;
    this->s_z = 0.0;
    
    this->h_x = -z * this->s_y;
    this->h_y = z * this->s_x;
    this->h_z = (x * this->s_y) - (y * this->s_x);
}

void AcePlayer::boxclipmove(double dt, double time) {
    float offset, m;
    if (this->crouch)
    {
        offset = 0.45f;
        m = 0.9f;
    }
    else
    {
        offset = 0.9f;
        m = 1.35f;
    }

    float f = dt * 32.f;
    float nx = f * this->v_x + this->p_x;
    float ny = f * this->v_y + this->p_y;
    float nz = this->p_z + offset;

    bool climb = false;
    if (this->v_x < 0) f = -0.45f;
    else f = 0.45f;
    float z = m;
    while (z >= -1.36f && !clipbox(this->map, nx + f, this->p_y - 0.45f, nz + z) && !clipbox(this->map, nx + f, this->p_y + 0.45f, nz + z))
        z -= 0.9f;
    if (z<-1.36f) this->p_x = nx;
    else if (!this->crouch && this->f_z<0.5f && !this->sprint)
    {
        z = 0.35f;
        while (z >= -2.36f && !clipbox(this->map, nx + f, this->p_y - 0.45f, nz + z) && !clipbox(this->map, nx + f, this->p_y + 0.45f, nz + z))
            z -= 0.9f;
        if (z<-2.36f)
        {
            this->p_x = nx;
            climb = true;
        }
        else this->v_x = 0;
    }
    else this->v_x = 0;

    if (this->v_y < 0) f = -0.45f;
    else f = 0.45f;
    z = m;
    while (z >= -1.36f && !clipbox(this->map, this->p_x - 0.45f, ny + f, nz + z) && !clipbox(this->map, this->p_x + 0.45f, ny + f, nz + z))
        z -= 0.9f;
    if (z<-1.36f) this->p_y = ny;
    else if (!this->crouch && this->f_z<0.5f && !this->sprint && !climb)
    {
        z = 0.35f;
        while (z >= -2.36f && !clipbox(this->map, this->p_x - 0.45f, ny + f, nz + z) && !clipbox(this->map, this->p_x + 0.45f, ny + f, nz + z))
            z -= 0.9f;
        if (z<-2.36f)
        {
            this->p_y = ny;
            climb = true;
        }
        else this->v_y = 0;
    }
    else if (!climb)
        this->v_y = 0;

    if (climb)
    {
        this->v_x *= 0.5f;
        this->v_y *= 0.5f;
        this->lastclimb = time;
        nz--;
        m = -1.35f;
    }
    else
    {
        if (this->v_z < 0)
            m = -m;
        nz += this->v_z*dt*32.f;
    }

    this->airborne = true;

    if (clipbox(this->map, this->p_x - 0.45f, this->p_y - 0.45f, nz + m) ||
        clipbox(this->map, this->p_x - 0.45f, this->p_y + 0.45f, nz + m) ||
        clipbox(this->map, this->p_x + 0.45f, this->p_y - 0.45f, nz + m) ||
        clipbox(this->map, this->p_x + 0.45f, this->p_y + 0.45f, nz + m))
    {
        if (this->v_z >= 0)
        {
            this->wade = this->p_z > 61;
            this->airborne = false;
            this->v_z = 0;
        }
        else
        {
            nz = this->p_z;
            this->v_z = 0;
        }
    }
    else
        this->p_z = nz - offset;

    reposition(dt, time);
}

void AcePlayer::reposition(double dt, double time) {
    // Set eye position
    this->e_x = this->p_x;
    this->e_y = this->p_y;
    this->e_z = this->p_z;
    
    double height = this->crouch ? 0.45f : 0.9f;
    this->e_z -= height;
}

bool AceGrenade::update(double dt, double time) {
    double eta;
    double nx, ny, nz;
    Vector pos;
    
    if (this->next_collision(dt, dt, &eta, &nx, &ny, &nz)) {
        pos = Vector(nx, ny, nz);
        
        // Apply impact to grenade
        Vector v = this->getVelocity();
        
        // Get normal
        Vector normal(0, 0, 0);
        if (pos.x - this->p_x < -0.1f) normal.x = 1;
        else if (pos.x - this->p_x > 0.1f) normal.x = -1;
        else if (pos.y - this->p_y < -0.1f) normal.y = 1;
        else if (pos.y - this->p_y > 0.1f) normal.y = -1;
        else if (pos.z - this->p_z < -0.1f) normal.z = 1;
        else if (pos.z - this->p_z > 0.1f) normal.z = -1;
        else return true; // stuck in a block
        
        // Adjust position and velocity
        double bounce = -0.36;
        v.x += normal.x * v.x * bounce * 2;
        v.y += normal.y * v.y * bounce * 2;
        v.z += normal.z * v.z * bounce * 2;
        
        this->setPosition(pos);
        this->setVelocity(v);
        
        // Continue movement with adjusted velocity
        return this->update(dt - eta, time);
    }
    
    this->p_x += this->v_x * dt;
    this->p_y += this->v_y * dt;
    this->p_z += this->v_z * dt;
    
    this->v_z += dt * 32.0; // Gravity
    
    // Air friction
    double f = 1 + dt;
    this->v_x /= f;
    this->v_y /= f;
    this->v_z /= f;
    
    return false; // Not hit solid
}

bool AceGrenade::next_collision(double dt, double max, double *eta, double *px, double *py, double *pz) {
    double step = dt;
    Vector p = this->getPosition();
    Vector v = this->getVelocity();
    
    if (dt > max) step = max;
    
    double tEnd = step * 32.0;
    double t = 0;
    double tDelta = tEnd / 8.0;
    
    while (t < tEnd) {
        Vector next = Vector(p.x + v.x * t / 32.0, p.y + v.y * t / 32.0, p.z + v.z * t / 32.0);
        if (clipbox(this->map, next.x, next.y, next.z)) {
            *eta = t / 32.0;
            *px = next.x;
            *py = next.y;
            *pz = next.z;
            return true;
        }
        t += tDelta;
    }
    
    return false;
}

bool cast_ray(AceMap *map, double px, double py, double pz, double dx, double dy, double dz, 
             long *x, long *y, long *z, float length, bool isdirection) {
    Vector p(px, py, pz);
    Vector d(dx, dy, dz);
    
    // Implementation as needed to cast a ray and return hit location
    
    return false; // Not implemented fully
}
