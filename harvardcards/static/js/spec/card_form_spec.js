define(['lodash', 'jquery', 'views/CardForm'], function(_, $, CardForm) {
    var getFixture = function() {
        var htmlFixture = '<form method="post" action=""><div class="message"></div><input type="submit" name="submit" value="Submit" /></form>';
        return $('<div>').html(htmlFixture);
    };

    var getCardFormWithFixture = function() {
        var fixture = getFixture();
        var formEl = fixture;
        var formMessageEl = fixture.find('.message');
        var card_form = new CardForm({formEl: formEl, formMessageEl: formMessageEl});
        card_form.init();
        return card_form;
    };

    describe("CardForm", function() {
        it("throws error on invalid config", function() {
            var factory = function(config) {
                return function() {
                    new CardForm(config);
                };
            };
            expect(factory()).toThrow();
            expect(factory({})).toThrow();
            expect(factory({formEl:'',formMessageEl:''})).toThrow();
            expect(factory({formEl:'.foo',formMessageEl:'.bar'})).not.toThrow();
        });

        it("constructs an object", function() {
            var card_form = getCardFormWithFixture();
            expect(card_form.formEl).toBeTruthy();
            expect(card_form.formMessageEl).toBeTruthy();
        });

        describe("messages", function() {
            var msg_map = [{
                testName: "shows info message before submitting", 
                testFunction:'beforeSubmit', 
                expectedMsgType:CardForm.MSG_INFO
            },{
                testName: "shows success message on success",
                testFunction:'success',
                expectedMsgType:CardForm.MSG_SUCCESS
            },{
                testName: "shows error message on errror", 
                testFunction:'error', 
                expectedMsgType:CardForm.MSG_ERROR
            }];
            _.each(msg_map, function(item) {
                var fn = item.testFunction;
                var msgType = item.expectedMsgType;

                it(item.testName, function() {
                    var card_form = getCardFormWithFixture();
                    spyOn(card_form, 'msg');
                    card_form[fn]();
                    expect(card_form.msg).toHaveBeenCalled();
                    expect(card_form.msg.mostRecentCall.args[1]).toBe(msgType);
                });
            });
        });
    });
});
