# coding:utf-8 
from django import  forms

from dbmanager.models import HostList
import re

class HostListForm(forms.ModelForm):
	class Meta:
		model = HostList
		fields = ['group','addip']

	def clean_addip(self):
		"""
		验证IP地址 是否合法
		"""
		addip =self.cleaned_data['addip']
		REGEX_ADDIP = "[\d^\.]+"
		p = re.compile(REGEX_ADDIP)
		if p.match(addip):
			return addip
		else:
			raise forms.ValidationError(u"IP地址输入非法",code="addip_invaild")

