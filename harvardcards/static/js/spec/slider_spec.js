define(['lodash','jquery','components/slider/slider'], function(_, $, Slider) {

	// Creates markup for a single element with an attached module.
	function getSlideHTML(size) {
		var items = _.map(_.range(0, size), function() {
			return '<li><a href="#"></a></li>';
		}).join('');
		return '<ul>' + items  + '</ul>';
	}

	function getFixture(size) {
		return $('<div class="slider"/>').html(getSlideHTML(size));
	}

	describe("Slider", function() {
		it("creates an instance with items", function() {
			var num_items = 3;
			var fixture = getFixture(num_items);
			var slider = new Slider({ el: fixture });

			// Compare the DOM elements (*not* jQuery objects) for equality
			expect(slider.el.get(0)).toBe(fixture.get(0));
			expect(slider.containerEl.get(0)).toBe(fixture.find("ul").get(0));
			fixture.find("li").each(function(index, el) {
				expect(slider.items[index]).toBe(el);
			});

			// Check the slider's knowledge
			expect(slider.getWidth()).toBe(fixture.width());
			expect(slider.getNumItems()).toBe(num_items);
			expect(slider.getLastIndex()).toBe(num_items - 1);
			expect(slider.getCurrentIndex()).toBe(0);
			expect(slider.isLastItem()).toBeFalsy();
			expect(slider.isFirstItem()).toBeTruthy();
		});

		it("creates an instance with a start index", function() {
			var num_items = 3;
			var valid_start = num_items - 1;
			var fixture = getFixture(num_items);
			var make_slider = function(start) {
				return function() {
					return new Slider({ el: fixture, startIndex: start });
				};
			};

			var slider_func = make_slider(valid_start);

			// slider with a valid start index
			expect(slider_func).not.toThrow();
			expect(slider_func().getCurrentIndex()).toBe(valid_start);

			// slider with an invalid start index
			expect(make_slider(num_items)).toThrow();
			expect(make_slider(num_items + 1)).toThrow();
		});

		it("creates an instance with plugins", function() {
			var fixture = getFixture(3);
			var slider = new Slider({
				el: fixture,
				plugins: {
					touch: null,
					responsive: null,
					keyboard: null
				}
			});
			expect(slider.pluginMap.responsive).toBeTruthy();
			expect(slider.pluginMap.touch).toBeTruthy();
			expect(slider.pluginMap.keyboard).toBeTruthy();
		});

		it("knows how to go to items", function() {
			var num_items = 10;
			var mid_index = Math.floor(num_items / 2);
			var fixture = getFixture(num_items);
			var slider = new Slider({ el: fixture });
			var success;

			expect(slider.isFirstItem()).toBeTruthy();
			expect(slider.isLastItem()).toBeFalsy();

			success = slider.goToPrev();
			expect(success).toBeFalsy();
			expect(slider.getCurrentIndex()).toBe(0);

			success = slider.goToNext();
			expect(success).toBeTruthy();
			expect(slider.getCurrentIndex()).toBe(1);

			success = slider.goToPrev();
			expect(success).toBeTruthy();
			expect(slider.getCurrentIndex()).toBe(0);

			success = slider.goToLast();
			expect(success).toBeTruthy();
			expect(slider.getCurrentIndex()).toBe(num_items - 1);
			expect(slider.isFirstItem()).toBeFalsy();
			expect(slider.isLastItem()).toBeTruthy();

			success = slider.goToNext();
			expect(success).toBeFalsy();

			success = slider.goTo(mid_index);
			expect(success).toBeTruthy();
			expect(slider.getCurrentIndex()).toBe(mid_index);

			success = slider.goToCurrent();
			expect(success).toBeTruthy();
			expect(slider.getCurrentIndex()).toBe(mid_index);
		});

		it("triggers slide and beforeslide events when going to an item", function() {
			var num_items = 5;
			var fixture = getFixture(num_items);
			var slider = new Slider({ el: fixture });
			var my = {
				onBeforeSlide: function() {},
				onSlide: function() {}
			};
			spyOn(my, 'onBeforeSlide');
			spyOn(my, 'onSlide');

			slider.bind("beforeslide", my.onBeforeSlide);
			slider.bind("slide", my.onSlide);

			while(!slider.isLastItem()) {
				slider.goToNext();
				expect(my.onBeforeSlide).toHaveBeenCalled();
				expect(my.onSlide).toHaveBeenCalled();
			}

			expect(my.onBeforeSlide.callCount).toBe(num_items - 1);
			expect(my.onSlide.callCount).toBe(num_items - 1);
		});
	});
});