'''Module for generation of tracks.'''
import numpy as np
from ..config import CONFIG
from ..detector_characteristics import DETECTOR_CHARACTERISTICS

RADIUS = float(CONFIG['Track Generation']['BoundingSphereRadius'])
TIMESTEP = int(CONFIG['Track Generation']['Timestep'])
SAMPLE_PADDING = int(CONFIG['Track Generation']['SamplePadding'])
SENSOR_RADIUS = float(CONFIG['Detector Config']['SensorRadius'])

def sample_spherical(ndim=3, n_vecs=1):
    '''pick a random point on a unit sphere'''
    vec = np.random.randn(ndim, n_vecs)
    vec /= np.linalg.norm(vec, axis=0)
    return vec

def generate_tracks(vel, t_entry, radius=RADIUS,):
    '''Return tracks with entry and exit vectors in local coords (x=north, y=east, z=up),
    and entry & exit time. vel is an array of velocities. t_entry is an array of time.
    Times should be in nanoseconds unix time.
    def generate_tracks(vel, t_entry):
        return entry_vecs, exit_vecs, t_entry, t_exit
    '''
    n_vecs = len(vel)
    if n_vecs != len(t_entry):
        raise ValueError('vel and t_entry array lengths not equal!')
    entry_vecs = sample_spherical(n_vecs=n_vecs)*radius
    exit_vecs = sample_spherical(n_vecs=n_vecs)*radius
    lengths = np.linalg.norm(entry_vecs-exit_vecs, axis=0)
    t_exit = lengths/vel
    return entry_vecs, exit_vecs, t_entry, t_exit

def acceleration_function(radius, mass, grav_const, sensor_radius=SENSOR_RADIUS):
    '''acceleration vector from G, M, and vector r.'''
    distances = np.sqrt(np.einsum('ij,ij->i', radius, radius))
    distances = np.minimum(distances, sensor_radius)
    return (grav_const*mass/distances**3)[:, np.newaxis]*radius

def generate_acceleration_dict(entry_vecs, exit_vecs, t_entry, t_exit, particle_properties,
                               timestep=TIMESTEP, padding=SAMPLE_PADDING):
    '''
    def generate_acceleration_dict(entry_vecs, exit_vecs, t_entry, t_exit, particle_properties,
                                   timestep=TIMESTEP, padding=SAMPLE_PADDING):
        return output
    output is structured as a list. Each element of the list corresponds to a single track.
    Each track consists of a dict, with the sensor name as the key.
    The value in the dict corresponding to each sensor name would be a numpy array of the
    accelerations. There would also be a 'time' value corresponding to the sample times.
    '''
    t_entry = t_entry*1e9
    t_exit = t_exit*1e9
    output = []
    for i, entry_vec in enumerate(entry_vecs.T):
        initial_sample_time = int(t_entry[i]) - int(t_entry[i])%timestep-padding*timestep
        vel_vector = (exit_vecs.T[i]-entry_vec)/(t_exit[i]+t_entry[i])
        final_sample_time = int(t_exit[i]) - int(t_exit[i])%timestep+(padding+1)*timestep
        n_samples = (final_sample_time - initial_sample_time)//timestep + 1
        sample_times = np.linspace(
            initial_sample_time,
            final_sample_time,
            n_samples,
            dtype='int'
        )
        initial_position = entry_vec-vel_vector*(int(t_entry[i])%timestep+padding*timestep)
        positions = np.matmul(
            np.array([(sample_times - initial_sample_time)]).T, np.array([vel_vector])
        ) + initial_position
        track_dict = {}
        track_dict['time'] = sample_times
        track_dict['particle_location'] = positions
        for key in DETECTOR_CHARACTERISTICS:
            rot_mat = DETECTOR_CHARACTERISTICS[key]['orientation']
            sensor_pos = DETECTOR_CHARACTERISTICS[key]['position']
            pos_diff = positions-sensor_pos
            accels = acceleration_function(
                pos_diff,
                particle_properties['M'],
                particle_properties['G']
            )
            rotated_accels = np.matmul(rot_mat, accels.T).T
            track_dict[key] = rotated_accels
        output.append(track_dict)
    return output
