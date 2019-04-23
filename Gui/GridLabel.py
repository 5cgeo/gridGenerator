from builtins import str, range, abs, round
from math import floor, ceil, pow
from qgis.core import QgsProject, QgsVectorLayer, QgsCoordinateTransform, QgsCoordinateReferenceSystem, QgsFillSymbol, QgsPoint, QgsGeometry, QgsGeometryGeneratorSymbolLayer
from qgis.core import QgsRuleBasedLabeling, QgsPalLayerSettings, QgsTextFormat, QgsPropertyCollection
from PyQt5.QtGui import QColor, QFont


class GridAndLabelCreator(object):
	def __init__(self, parent=None):
		
		super(GridLabel, self).__init__(parent)


	def geo_test(layer):
		
		if layer.crs().isGeographic() == False:
			self.iface.messageBar().pushMessage("Error", "Layer CRS is not geographic, please transform to a geographic CRS", level=Qgis.Critical)
			return False
		
		pass
	
	
	def utm_Symb_Generator (grid_spacing, trUTMLL, trLLUTM, grid_symb, properties, geo_number_x, geo_number_y, UTM_num_x, UTM_num_y, t, u, xmin_source, xmax_source, ymin_source, ymax_source, xmin_UTM, xmax_UTM, ymin_UTM, ymax_UTM):
		
		test_line = [None]*2
		symb = QgsGeometryGeneratorSymbolLayer.create(properties)
		symb.setSymbolType(1)

		#Test First And Last Grid Lines
		#Vertical
		if (t == 1 and u == 0) or (t == UTM_num_x and u == 0):
			
			#Symbol vertices
			v1 = QgsPoint(((floor(xmin_UTM/grid_spacing)+t)*grid_spacing),((floor(ymin_UTM/grid_spacing)+1)*grid_spacing))
			v1.transform(trUTMLL)
			v2 = QgsPoint(((floor(xmin_UTM/grid_spacing)+t)*grid_spacing),((floor(ymax_UTM/grid_spacing)+1)*grid_spacing))
			v2.transform(trUTMLL)
			
			#0: left bound; 1: right bound
			test_line[0] = QgsGeometry.fromWkt('LINESTRING ('+str(xmin_source)+' '+str(ymin_source)+','+str(xmin_source)+' '+str(ymax_source)+')')
			test_line[1] = QgsGeometry.fromWkt('LINESTRING ('+str(xmax_source)+' '+str(ymin_source)+','+str(xmax_source)+' '+str(ymax_source)+')')
			test_grid = QgsGeometry.fromPolyline([v1,v2])
			if test_line[0].intersects(test_grid):
				mid_point = test_line[0].intersection(test_grid).vertexAt(0)
				if v1.x() > v2.x():
					symb.setGeometryExpression('make_line(make_point('+str(v1.x())+','+str(ymin_source)+'), make_point('+str(mid_point.x())+','+str(mid_point.y())+'))')
				else:
					symb.setGeometryExpression('make_line(make_point('+str(mid_point.x())+','+str(mid_point.y())+'), make_point('+str(v2.x())+','+str(ymax_source)+'))')
			elif test_line[1].intersects(test_grid):
				mid_point = test_line[1].intersection(test_grid).vertexAt(0)
				if v1.x() < v2.x():
					symb.setGeometryExpression('make_line(make_point('+str(v1.x())+','+str(ymin_source)+'), make_point('+str(mid_point.x())+','+str(mid_point.y())+'))')
				else:
					symb.setGeometryExpression('make_line(make_point('+str(mid_point.x())+','+str(mid_point.y())+'), make_point('+str(v2.x())+','+str(ymax_source)+'))')
			else:
				symb.setGeometryExpression('make_line(make_point('+str(v1.x())+','+str(ymin_source)+'), make_point('+str(v2.x())+','+str(ymax_source)+'))')
		
		#Horizontal
		elif (u == 1 and t == 0) or (u == UTM_num_y and t == 0):
			
			#Symbol vertices
			h1 = QgsPoint(((floor(xmin_UTM/grid_spacing)+1)*grid_spacing),((floor(ymin_UTM/grid_spacing)+u)*grid_spacing))
			h1.transform(trUTMLL)
			h2 = QgsPoint(((floor(xmax_UTM/grid_spacing)+1)*grid_spacing),((floor(ymin_UTM/grid_spacing)+u)*grid_spacing))
			h2.transform(trUTMLL)
			
			#0: bottom bound; 1: upper bound
			test_line[0] = QgsGeometry.fromWkt('LINESTRING ('+str(xmin_source)+' '+str(ymin_source)+','+str(xmax_source)+' '+str(ymin_source)+')')
			test_line[1] = QgsGeometry.fromWkt('LINESTRING ('+str(xmin_source)+' '+str(ymax_source)+','+str(xmax_source)+' '+str(ymax_source)+')')
			test_grid = QgsGeometry.fromPolyline([h1,h2])
			if test_line[0].intersects(test_grid):
				mid_point = test_line[0].intersection(test_grid).vertexAt(0)
				if h1.y() > h2.y():
					symb.setGeometryExpression('make_line(make_point('+str(xmin_source)+','+str(h1.y())+'), make_point('+str(mid_point.x())+','+str(mid_point.y())+'))')
				else:
					symb.setGeometryExpression('make_line(make_point('+str(mid_point.x())+','+str(mid_point.y())+'), make_point('+str(xmax_source)+','+str(h2.y())+'))')
			elif test_line[1].intersects(test_grid):
				mid_point = test_line[1].intersection(test_grid).vertexAt(0)
				if h1.y() < h2.y():
					symb.setGeometryExpression('make_line(make_point('+str(xmin_source)+','+str(h1.y())+'), make_point('+str(mid_point.x())+','+str(mid_point.y())+'))')
				else:
					symb.setGeometryExpression('make_line(make_point('+str(mid_point.x())+','+str(mid_point.y())+'), make_point('+str(xmax_source)+','+str(h2.y())+'))')
			else:
				symb.setGeometryExpression("make_line(make_point("+str(xmin_source)+","+str(h1.y())+"), make_point("+str(xmax_source)+","+str(h2.y())+"))")
		
		#Inner Grid Lines
		
		#Vertical
		elif (not(t == 1)) and (not(t == UTM_num_x)) and u == 0:
			v1 = QgsPoint(((floor(xmin_UTM/grid_spacing)+t)*grid_spacing),((floor(ymin_UTM/grid_spacing)+1)*grid_spacing))
			v1.transform(trUTMLL)
			v2 = QgsPoint(((floor(xmin_UTM/grid_spacing)+t)*grid_spacing),((floor(ymax_UTM/grid_spacing)+1)*grid_spacing))
			v2.transform(trUTMLL)
			symb.setGeometryExpression('make_line(make_point('+str(v1.x())+','+str(ymin_source)+'), make_point('+str(v2.x())+','+str(ymax_source)+'))')
		
		#Horizontal
		elif (not(u == 1)) and (not(u == UTM_num_y)) and t == 0:
			h1 = QgsPoint(((floor(xmin_UTM/grid_spacing)+1)*grid_spacing),((floor(ymin_UTM/grid_spacing)+u)*grid_spacing))
			h1.transform(trUTMLL)
			h2 = QgsPoint(((floor(xmax_UTM/grid_spacing)+1)*grid_spacing),((floor(ymin_UTM/grid_spacing)+u)*grid_spacing))
			h2.transform(trUTMLL)
			symb.setGeometryExpression("make_line(make_point("+str(xmin_source)+","+str(h1.y())+"), make_point("+str(xmax_source)+","+str(h2.y())+"))")

		grid_symb.appendSymbolLayer(symb)
		return grid_symb


	def grid_Labeler (coord_base_x, coord_base_y, px, py, u, t, dx, dy, vAlign, hAlign, desc, fSize, fontType, expression_str):
		
		x = coord_base_x + px*u
		y = coord_base_y + py*t
		
		#Label Format Settings
		settings = QgsPalLayerSettings()
		settings.Placement = QgsPalLayerSettings.Free
		settings.isExpression = True
		textprop = QgsTextFormat()
		textprop.setColor(QColor(0,0,0,255))
		textprop.setSize(fSize)
		textprop.setFont(QFont(fontType))
		textprop.setLineHeight(1)
		settings.setFormat(textprop)

		#Label Name and Position
		settings.fieldName = expression_str
		datadefined = QgsPropertyCollection()
		datadefined.setProperty(9, (x + dx))
		datadefined.setProperty(10, (y + dy))
		if not(hAlign == ''):
			datadefined.setProperty(11, hAlign)
		if not(vAlign == ''):
			datadefined.setProperty(12, vAlign)

		#Creating and Activating Labeling Rule
		settings.setDataDefinedProperties(datadefined)
		rule = QgsRuleBasedLabeling.Rule(settings)
		rule.setDescription(desc)
		rule.setActive(True)
		
		return rule

	def UTM_Grid_labeler (x_UTM, y_UTM, x_geo, y_geo, x_min, y_min, px, py, trUTMLL, trLLUTM, u, isVertical, dx, dy, dyO, dy1, label_index, vAlign, hAlign, desc, fSize, fontType, grid_spacing, map_scale):

		# Check if is labeling grid's vertical lines
		if isVertical:
			x = QgsPoint(((floor(x_UTM/grid_spacing)+u)*grid_spacing),y_UTM)
			x.transform(trUTMLL)
			x = x.x()+dx

			# Displacing UTM Label it overlaps with Geo Label
			y = y_geo
			test = QgsPoint(((floor(x_UTM/grid_spacing)+u)*grid_spacing),y_UTM)
			test.transform(trUTMLL)
			testif = abs(floor(abs(round(test.x(), 4) - (x_min % (px)) - (0.001 *map_scale/10000))/px) - floor(abs(round(test.x(), 4) - (x_min % (px)) + (0.001 *map_scale/10000))/px))
			if testif >= 1:
				y = y+dyO
			else:
				y = y+dy

			full_label = str((floor(x_UTM/grid_spacing)+u)*grid_spacing)
			if label_index == 1:
				expression_str = full_label[ : len( full_label )-5]
			elif label_index == 2:
				expression_str = str('\'')+full_label[len( full_label )-5 : -3]+str('\'')
				fSize = 7.08*fSize/4.25
			elif label_index == 3:
				expression_str = str('\'')+full_label[-3 : ]+str('\'')
		# Labeling grid's horizontal lines
		else:
			x = x_geo+dx
			# Displacing UTM Label it overlaps with Geo Label
			y = QgsPoint(x_UTM,(floor(y_UTM/grid_spacing)+u)*grid_spacing)
			y.transform(trUTMLL)
			y = y.y()
			test = QgsPoint(x_UTM,(floor(y_UTM/grid_spacing)+u)*grid_spacing)
			test.transform(trUTMLL)
			testif = abs(floor(abs(round(test.y(), 4) - (y_min % (py)) - (0.0004 *map_scale/10000))/py) - floor(abs(round(test.y(), 4) - (y_min % (py)))/py))
			if testif >= 1:
				y = y+dy1
			else:
				testif2 = abs(floor(abs(round(test.y(), 4) - (y_min % (py)))/py) - floor(abs(round(test.y(), 4) - (y_min % (py)) + (0.0004 *map_scale/10000))/py))
				if testif2 >= 1:
					y = y+dyO
				else:
					y = y+dy
			
			full_label = str((floor(y_UTM/grid_spacing)+u)*grid_spacing)
			if label_index == 1:
				expression_str = full_label[ : len( full_label )-5]
			elif label_index == 2:
				expression_str = str('\'')+full_label[len( full_label )-5 : -3]+str('\'')
				fSize = 7.08*fSize/4.25
			elif label_index == 3:
				expression_str = str('\'')+full_label[-3 : ]+str('\'')
    
		# Label Format Settings
		settings = QgsPalLayerSettings()
		settings.Placement = QgsPalLayerSettings.Free
		settings.isExpression = True
		textprop = QgsTextFormat()
		textprop.setColor(QColor(0,0,0,255))
		textprop.setSize(fSize)
		textprop.setFont(QFont(fontType))
		textprop.setLineHeight(1)
		settings.setFormat(textprop)

		# Label Name and Position
		settings.fieldName = expression_str
		datadefined = QgsPropertyCollection()
		datadefined.setProperty(9, x)
		datadefined.setProperty(10, y)
		if not(hAlign == ''):
			datadefined.setProperty(11, hAlign)
		if not(vAlign == ''):
			datadefined.setProperty(12, vAlign)
		# Creating and Activating Labeling Rule
		settings.setDataDefinedProperties(datadefined)
		rule = QgsRuleBasedLabeling.Rule(settings)
		rule.setDescription(desc)
		rule.setActive(True)
		#Exit: Label Rule
		return rule



	def Conv_dec_gms (base_coord, coord_spacing, u, neg_character, pos_character):
		
		x = base_coord + coord_spacing*u
		conv_exp_str = 'concat(floor(round(abs('+str(x)+'),4)),'+str('\'º\'')+','+str('\' \'')+',floor(round((-floor(round(abs('+str(x)+'),4))+round(abs('+str(x)+'),4)),4)*60),'+str('\'\'\'\'')+','+str('\' \'')+',round((round((-floor(round(abs('+str(x)+'),4))+round(abs('+str(x)+'),4)),4)*60-floor(round((-floor(round(abs('+str(x)+'),4))+round(abs('+str(x)+'),4)),4)*60))*60),'+str('\'"\'')+',if('+str(x)+'<0, '+str('\' ')+neg_character+str('\'')+','+str('\' ')+pos_character+str('\'')+'))'
		
		return conv_exp_str



	def styleCreator (layer, index, spacing, crossX, crossY, scale, color, fontSize, font):
		
		grid_spacing = spacing
		geo_number_x = crossX
		geo_number_y = crossY
		map_scale = scale*1000
		grid_color = color
		fSize = fontSize
		fontType = font
		
		#Loading feature
		layer_bound = layer
		feature_bound = layer_bound.getFeature(0)

		#Getting Feature Source CRS and Geometry
		bound_sourcecrs = layer_bound.crs().authid()
		feature_bbox = feature_bound.geometry().boundingBox()
		GridAndLabelCreator.geo_test(layer_bound)
		geo_bound_bb = str(feature_bbox).replace(',','').replace('>','')

		#Defining CRSs Transformations
		inom = feature_bound[index]
		if inom[0]=='N': 
			bound_UTM = 'EPSG:319' + str(72 + int(inom[3:5])-18)
		elif inom[0]=='S': 
			bound_UTM = 'EPSG:319' + str(78 + int(inom[3:5])-18) 
		else:
			iface.messageBar().pushMessage("Error", "Invalid index attribute", level=Qgis.Critical)
			return
		trLLUTM = QgsCoordinateTransform(QgsCoordinateReferenceSystem(bound_sourcecrs), QgsCoordinateReferenceSystem(bound_UTM), QgsProject.instance())
		trUTMLL = QgsCoordinateTransform(QgsCoordinateReferenceSystem(bound_UTM), QgsCoordinateReferenceSystem(bound_sourcecrs), QgsProject.instance())

		#Defining UTM Grid Symbology Type
		renderer = layer_bound.renderer()
		properties = {'color': 'black'}
		grid_symb = QgsFillSymbol.createSimple(properties)


		""" Creating UTM Grid """
		geo_UTM = feature_bound.geometry()
		geo_UTM.transform(trLLUTM)
		bound_UTM_bb = str(geo_UTM.boundingBox()).replace(',','').replace('>','')
		xmin_source = float(geo_bound_bb.split()[1])
		ymin_source = float(geo_bound_bb.split()[2])
		xmax_source = float(geo_bound_bb.split()[3])
		ymax_source = float(geo_bound_bb.split()[4])
		xmin_UTM = float(bound_UTM_bb.split()[1])
		ymin_UTM = float(bound_UTM_bb.split()[2])
		xmax_UTM = float(bound_UTM_bb.split()[3])
		ymax_UTM = float(bound_UTM_bb.split()[4])
		UTM_num_x = floor(xmax_UTM/grid_spacing) - floor(xmin_UTM/grid_spacing)
		UTM_num_y = floor(ymax_UTM/grid_spacing) - floor(ymin_UTM/grid_spacing)

		#Generating Vertical Lines
		for x in range(1, UTM_num_x+1):
			grid_symb= GridAndLabelCreator.utm_Symb_Generator (grid_spacing, trUTMLL, trLLUTM, grid_symb, properties, geo_number_x, geo_number_y, UTM_num_x, UTM_num_y, x, 0, xmin_source, xmax_source, ymin_source, ymax_source, xmin_UTM, xmax_UTM, ymin_UTM, ymax_UTM)

		#Generating Horizontal Lines
		for y in range(1, UTM_num_y+1):
			grid_symb = GridAndLabelCreator.utm_Symb_Generator (grid_spacing, trUTMLL, trLLUTM, grid_symb, properties, geo_number_x, geo_number_y, UTM_num_x, UTM_num_y, 0, y, xmin_source, xmax_source, ymin_source, ymax_source, xmin_UTM, xmax_UTM, ymin_UTM, ymax_UTM)


		""" Creating Geo Grid """
		px = (xmax_source-xmin_source)/(geo_number_x+1)
		py = (ymax_source-ymin_source)/(geo_number_y+1)

		#Generating Crosses
		for u in range(1, (geo_number_x+2)):
			for t in range(0, (geo_number_y+2)):
				symb = QgsGeometryGeneratorSymbolLayer.create(properties)
				symb.setSymbolType(1)
				symb.setGeometryExpression('make_line(make_point('+str(xmin_source+px*u)+',('+str(ymin_source+py*t)+')),make_point('+str(xmin_source+px*u-(0.0003215*map_scale/10000))+',('+str(ymin_source+py*t)+')))')
				grid_symb.appendSymbolLayer(symb)
		for u in range(0, (geo_number_x+2)):
			for t in range(1, (geo_number_y+2)):
				symb = QgsGeometryGeneratorSymbolLayer.create(properties)
				symb.setSymbolType(1)
				symb.setGeometryExpression('make_line(make_point('+str(xmin_source+px*u)+',('+str(ymin_source+py*t)+')),make_point('+str(xmin_source+px*u)+',('+str(ymin_source+py*t-(0.0003215*map_scale/10000))+')))')
				grid_symb.appendSymbolLayer(symb)
		for u in range(0, (geo_number_x+1)):
			for t in range(0, (geo_number_y+2)):
				symb = QgsGeometryGeneratorSymbolLayer.create(properties)
				symb.setSymbolType(1)
				symb.setGeometryExpression('make_line(make_point('+str(xmin_source+px*u+(0.0003215*map_scale/10000))+',('+str(ymin_source+py*t)+')),make_point('+str(xmin_source+px*u)+',('+str(ymin_source+py*t)+')))')
				grid_symb.appendSymbolLayer(symb)
		for u in range(0, (geo_number_x+2)):
			for t in range(0, (geo_number_y+1)):
				symb = QgsGeometryGeneratorSymbolLayer.create(properties)
				symb.setSymbolType(1)
				symb.setGeometryExpression('make_line(make_point('+str(xmin_source+px*u)+',('+str(ymin_source+py*t+(0.0003215*map_scale/10000))+')),make_point('+str(xmin_source+px*u)+',('+str(ymin_source+py*t)+')))')
				grid_symb.appendSymbolLayer(symb)


		""" Rendering UTM and Geographic Grid """
		grid_symb.deleteSymbolLayer(0)
		grid_symb.setColor(grid_color)
		renderer.setSymbol(grid_symb)
		
		
		""" Labeling Geo Grid """
		root_rule = QgsRuleBasedLabeling.Rule(QgsPalLayerSettings())
		map_scaleX = scale/10
		
		#Upper
		for u in range(0, geo_number_x+2):
			ruletemp = GridAndLabelCreator.grid_Labeler (xmin_source, ymax_source, px, py, u, 0, 0, (0.00015*map_scaleX), '', 'Center', 'Up '+str(u+1), fSize, fontType, GridAndLabelCreator.Conv_dec_gms(xmin_source, px, u, 'W', 'E'))
			root_rule.appendChild(ruletemp)

		#Bottom
		for b in range(0, geo_number_x+2):
			ruletemp = GridAndLabelCreator.grid_Labeler (xmin_source, ymin_source, px, py, b, 0, 0, (-0.00040*map_scaleX), '', 'Center', 'Bot '+str(b+1), fSize, fontType, GridAndLabelCreator.Conv_dec_gms(xmin_source, px, b, 'W', 'E'))
			root_rule.appendChild(ruletemp)

		#Right
		for r in range(0, geo_number_y+2):
			ruletemp = GridAndLabelCreator.grid_Labeler (xmax_source, ymin_source, px, py, 0, r, (0.00018*map_scaleX), 0, 'Half', '', 'Right '+str(r+1), fSize, fontType, GridAndLabelCreator.Conv_dec_gms(ymin_source, py, r, 'S', 'N'))
			root_rule.appendChild(ruletemp)

		#Left
		for l in range(0, geo_number_y+2):
			ruletemp = GridAndLabelCreator.grid_Labeler (xmin_source, ymin_source, px, py, 0, l, (-0.00120*map_scaleX), 0, 'Half', '', 'Left '+str(l+1), fSize, fontType, GridAndLabelCreator.Conv_dec_gms(ymin_source, py, l, 'S', 'N'))
			root_rule.appendChild(ruletemp)


		# Labeling UTM Grid
		for u in range(1, UTM_num_x+1):
			# Upper
			ruletemp = GridAndLabelCreator.UTM_Grid_labeler (xmin_UTM, ymax_UTM, 0, ymax_source, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, True, (-0.00030*map_scaleX), (0.00024*map_scaleX), (0.00052*map_scaleX), 0, 1, '', '', 'Up'+str(u), fSize, fontType, grid_spacing, map_scale)
			root_rule.appendChild(ruletemp)
			ruletemp = GridAndLabelCreator.UTM_Grid_labeler (xmin_UTM, ymax_UTM, 0, ymax_source, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, True, 0, (0.00012*map_scaleX), (0.00040*map_scaleX), 0, 2, '', 'Center', 'Up'+str(u), fSize, fontType, grid_spacing, map_scale)
			root_rule.appendChild(ruletemp)
			ruletemp = GridAndLabelCreator.UTM_Grid_labeler (xmin_UTM, ymax_UTM, 0, ymax_source, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, True, (0.00018*map_scaleX), (0.00024*map_scaleX), (0.00052*map_scaleX), 0, 3, '', '', 'Up'+str(u), fSize, fontType, grid_spacing, map_scale)
			root_rule.appendChild(ruletemp)
			# Bottom
			ruletemp = GridAndLabelCreator.UTM_Grid_labeler (xmin_UTM, ymin_UTM, 0, ymin_source, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, True,(-0.00030*map_scaleX), (-0.00028*map_scaleX), (-0.00053*map_scaleX), 0, 1, '', '', 'Bot'+str(u), fSize, fontType, grid_spacing, map_scale)
			root_rule.appendChild(ruletemp)
			ruletemp = GridAndLabelCreator.UTM_Grid_labeler (xmin_UTM, ymin_UTM, 0, ymin_source, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, True, 0, (-0.00039*map_scaleX), (-0.00065*map_scaleX), 0, 2, '', 'Center', 'Bot'+str(u), fSize, fontType, grid_spacing, map_scale)
			root_rule.appendChild(ruletemp)
			ruletemp = GridAndLabelCreator.UTM_Grid_labeler (xmin_UTM, ymin_UTM, 0, ymin_source, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, True, (0.00018*map_scaleX), (-0.00028*map_scaleX), (-0.00053*map_scaleX), 0, 3, '', '', 'Bot'+str(u), fSize, fontType, grid_spacing, map_scale)
			root_rule.appendChild(ruletemp)

		for u in range(1, UTM_num_y+1):
			# Left
			ruletemp = GridAndLabelCreator.UTM_Grid_labeler (xmin_UTM, ymin_UTM, xmin_source, 0, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, False, (-0.00110*map_scaleX), (-0.00003*map_scaleX), (0.00064*map_scaleX), (0.00032*map_scaleX), 1, '', '', 'Left'+str(u), fSize, fontType, grid_spacing, map_scale)
			root_rule.appendChild(ruletemp)
			ruletemp = GridAndLabelCreator.UTM_Grid_labeler (xmin_UTM, ymin_UTM, xmin_source, 0, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, False, (-0.00070*map_scaleX), (-0.00015*map_scaleX), (0.00052*map_scaleX), (0.00020*map_scaleX), 2, '', 'Center', 'Left'+str(u), fSize, fontType, grid_spacing, map_scale)
			root_rule.appendChild(ruletemp)
			ruletemp = GridAndLabelCreator.UTM_Grid_labeler (xmin_UTM, ymin_UTM, xmin_source, 0, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, False, (-0.00050*map_scaleX), (-0.00003*map_scaleX), (0.00064*map_scaleX), (0.00032*map_scaleX), 3, '', '', 'Left'+str(u), fSize, fontType, grid_spacing, map_scale)
			root_rule.appendChild(ruletemp)
			# Right
			ruletemp = GridAndLabelCreator.UTM_Grid_labeler (xmax_UTM, ymin_UTM, xmax_source, 0, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, False, (0.00010*map_scaleX), (-0.00003*map_scaleX), (0.00064*map_scaleX), (0.00032*map_scaleX), 1, '', '', 'Right'+str(u), fSize, fontType, grid_spacing, map_scale)
			root_rule.appendChild(ruletemp)
			ruletemp = GridAndLabelCreator.UTM_Grid_labeler (xmax_UTM, ymin_UTM, xmax_source, 0, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, False, (0.00050*map_scaleX), (-0.00015*map_scaleX), (0.00052*map_scaleX), (0.00020*map_scaleX), 2, '', 'Center', 'Right'+str(u), fSize, fontType, grid_spacing, map_scale)
			root_rule.appendChild(ruletemp)
			ruletemp = GridAndLabelCreator.UTM_Grid_labeler (xmax_UTM, ymin_UTM, xmax_source, 0, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, False, (0.00070*map_scaleX), (-0.00003*map_scaleX), (0.00064*map_scaleX), (0.00032*map_scaleX), 3, '', '', 'Right'+str(u), fSize, fontType, grid_spacing, map_scale)
			root_rule.appendChild(ruletemp)


		""" Activating Labels """
		rules = QgsRuleBasedLabeling(root_rule)
		layer_bound.setLabeling(rules)
		layer_bound.setLabelsEnabled(True)

		return

