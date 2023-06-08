from django import template

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_names):
    group_names_arr = group_names.split(",")
    return user.groups.filter(name__in=group_names_arr).exists() 