from ui.mobile_shell import build_mobile_shell as _build_mobile_shell


OLD_IS_REQUEST_PRICE = """  function isRequestPrice(stone){
    const price = Number(stone.price || stone.price_rub || stone.public_price_rub || 0);
    const status = String(stone.price_status || '').toLowerCase();
    const action = String(stone.public_action || '').toLowerCase();
    const checkoutEnabled = stone.checkout_enabled === true || String(stone.checkout_enabled).toLowerCase() === 'true';
    const publicSellable = stone.public_sellable === true || String(stone.public_sellable).toLowerCase() === 'true';
    return price <= 0 || ['request_price','missing','score_required','future_scope','blocked','needs_review','index_pending','index_suggested'].includes(status) || action === 'request_price' || !checkoutEnabled || !publicSellable;
  }"""


CONTRACT_FIRST_IS_REQUEST_PRICE = """  function hasComputedField(stone, field){
    return stone && Object.prototype.hasOwnProperty.call(stone, field) && stone[field] !== null && stone[field] !== undefined && String(stone[field]).trim() !== '';
  }

  function fieldIsFalse(stone, field){
    if(!hasComputedField(stone, field)) return false;
    const value = stone[field];
    return value === false || String(value).toLowerCase() === 'false' || String(value) === '0';
  }

  function fieldIsTrue(stone, field){
    if(!hasComputedField(stone, field)) return false;
    const value = stone[field];
    return value === true || String(value).toLowerCase() === 'true' || String(value) === '1';
  }

  function isRequestPrice(stone){
    const price = Number(stone.price || stone.price_rub || stone.public_price_rub || 0);
    const status = String(stone.price_status || '').toLowerCase();
    const action = String(stone.public_action || '').toLowerCase();
    const hasAction = hasComputedField(stone, 'public_action');
    const hasCheckoutEnabled = hasComputedField(stone, 'checkout_enabled');
    const hasPublicSellable = hasComputedField(stone, 'public_sellable');

    if(hasAction && action === 'request_price') return true;
    if(hasAction && action === 'checkout'){
      if(hasCheckoutEnabled && fieldIsFalse(stone, 'checkout_enabled')) return true;
      if(hasPublicSellable && fieldIsFalse(stone, 'public_sellable')) return true;
      return price <= 0;
    }
    if(hasCheckoutEnabled && fieldIsFalse(stone, 'checkout_enabled')) return true;
    if(hasPublicSellable && fieldIsFalse(stone, 'public_sellable')) return true;
    if(hasCheckoutEnabled || hasPublicSellable || hasAction) return price <= 0;

    return price <= 0 || ['request_price','missing','score_required','future_scope','blocked','needs_review','index_pending','index_suggested'].includes(status);
  }"""


def build_mobile_shell(page: str, stones_json: str) -> str:
    html = _build_mobile_shell(page=page, stones_json=stones_json)
    return html.replace(OLD_IS_REQUEST_PRICE, CONTRACT_FIRST_IS_REQUEST_PRICE)
