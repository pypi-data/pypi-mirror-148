from pyacptrak import *
import pytest

#Test Segment
def test_seg_input():
	with pytest.raises(Exception) as e_info:
		Segment(2)

def test_seg_plot_1():
	with pytest.raises(Exception) as e_info:
		Segment('aa').plot('a')

def test_seg_plot_2():
	assert isinstance(Segment('aa').plot(20), Segment)

#Test Track
def test_track_input_seg():
	with pytest.raises(Exception) as e_info:
		Track([2,3])

def test_track_plot_1():
	with pytest.raises(Exception) as e_info:
		Track([Segment('aa'), Segment('ab')]).plot('a')

def test_track_plot_2():
	assert isinstance(TRACK180.plot(20), Track)

#Test Loop
def test_loop_length_1():
	assert Loop().info()['length'] == 3240

def test_loop_length_2():
	assert Loop(3,3).info()['length'] == 7200

def test_loop_plot_1():
	with pytest.raises(Exception) as e_info:
		Loop(3,3).plot('a')

def test_loop_plot_2():
	assert isinstance(Loop(3,3).plot(20), Loop)

#Test Assembly





