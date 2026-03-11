#!/usr/bin/env python

# Created by: Moksh Chitkara
# Last Update: Mar 10th 2026
# v1.0.0
# Copyright (C) 2026  Moksh Chitkara
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Global Variables
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()

################################################################################################
# Window creation #
###################
def main_ui():
	# vertical group
	window = [ui.VGroup({"Spacing": 15,},[
			# horizontal groups
			# Track Select
			ui.HGroup({ 'Weight': 0 }, [
				ui.Label({'Text': "Scale amount: "}),
				ui.LineEdit({'ID': "scale_edit", "Text": "1.00"}),
			]),
			# Checkbox to delete marker
			ui.HGroup({ 'Weight': 0 }, [
				ui.CheckBox({"ID": "x_check", "Text": "Scale X-Axis", "Checked": False}),
				ui.CheckBox({"ID": "y_check", "Text": "Scale Y-Axis", "Checked": True}),
			]),
			# Button to start
			ui.HGroup({ 'Weight': 0 }, [
				ui.VGap(),
				ui.Button({"ID": "Start", "Text": "Begin Scaling", "Weight": 0}),
				ui.VGap()
			]),
			]) 
		]
	return window

ui = fu.UIManager # get UI utility from fusion
disp = bmd.UIDispatcher(ui) # gets display settings?

# window definition
window = disp.AddWindow({"WindowTitle": "Scale Transform",
			"ID": "STWin", 
			'WindowFlags': {'Window': True,'WindowStaysOnTopHint': True},
			"Geometry": [1500,500,200,120], # x-position, y-position, width, height
			}, 
			main_ui())

itm = window.GetItems() # Grabs all UI elements to be manipulated
################################################################################################
# Functions #
#############

def _main(ev):

	itm['Start'].Enabled = False
	itm['Start'].Text = "Starting..."
	
	timeline = project.GetCurrentTimeline()
	
	for track in range(1, timeline.GetTrackCount("video")+1):
		if not timeline.GetIsTrackLocked("video", track):
			prog = 0
			total = len(timeline.GetItemListInTrack("video",track))
			for clip in timeline.GetItemListInTrack("video",track):
				prog += 1
				loading = "{:.2%}".format(float(prog)/float(total))
				itm['Start'].Text = "Track {}: {}".format(track, loading)
				if clip.GetClipEnabled():
					try:
						if clip.GetMediaPoolItem():
							if itm["x_check"].Checked and (clip.GetProperty('Pan') != 0.0):
								propertyValue = float(clip.GetProperty('Pan')) * float(itm["scale_edit"].Text)
								print("[LOG] X Position scaled:", clip.GetName(),clip.SetProperty('Pan', round(propertyValue, 3)))
							if itm["y_check"].Checked  and (clip.GetProperty('Tilt') != 0.0):
								propertyValue = float(clip.GetProperty('Tilt')) * float(itm["scale_edit"].Text)
								print("[LOG] Y Position scaled:", clip.GetName(), clip.SetProperty('Tilt', round(propertyValue, 3)))
					except:
						print("[ERROR] Failed on", clip.GetName())
	itm['Start'].Text = "Begin Scaling"
	itm['Start'].Enabled = True

# needed to close window
def _close(ev):
	disp.ExitLoop()

################################################################################################
# GUI Elements #
# button presses
window.On.Start.Clicked = _main
window.On.STWin.Close = _close
window.Show()
disp.RunLoop()
window.Hide()
#################################################################################################
