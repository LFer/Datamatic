
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2014 Datamatic (http://www.datamatic.com.uy). All Rights Reserved
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from osv import osv
from osv import fields

class discs(osv.osv):

    _name = 'discs'
    _description = 'Discs Library'

    _columns = {
            'name':fields.char('Title', size=64, required=True,),
            'description':fields.text('Description', size=256),
            'year':fields.date('Published'),
            'format':fields.selection([('vinyl','Vinyl'),('cd','CD'),('mp3','Mp3'),('mp4','Mp4')],'Format'),
            'active':fields.boolean('Active'),
        }

    _defaults = {
                 'format': lambda *a: 'cd',
                 'active': lambda *a: True,
        }

discs()



