define(['jquery', 'lodash', 'bootstrap'], function($, _, bootstrap){
	var Field = function(label, field_type, field_id, display){
		this.label = label;
		this.field_type = field_type;
		this.field_id = field_id;
		this.display = display;
		var display_class = "display";
		if(display){
			display_class = "display";
		} else {
			display_class = "reveal";
		}
		
		if(field_type == 'T'){
			this.template = '<div class="field-template '+display_class+'"><span class="mylabel">'+label+'</span> '
				+ '<input class="text-field-template" data-id="'+field_id+'" type="text"/></div> ';
		} else if(field_type == 'I'){
			this.template = '<div class="field-template '+display_class+'"><span class="mylabel">'+label+'</span> '
				+ '<input class="img-field-template" data-id="'+field_id+'" type="text"/></div> ';
		} else {
			this.template = 'Not a valid type';
		}
	}
	
	_.extend(Field.prototype, {
		
	});
	
	return Field;
	

});