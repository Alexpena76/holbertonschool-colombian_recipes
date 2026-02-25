-- Colombian Recipe API - Database Initialization
-- Seeds: 6 categories + 3 recipes (Bandeja Paisa, Ajiaco, Arepas)

-- =====================================================
-- CATEGORIES
-- =====================================================
INSERT INTO categories (id, name, name_es, image_url) VALUES
('breakfast', 'Breakfast', 'Desayuno', '/images/categories/breakfast.jpg'),
('lunch', 'Lunch', 'Almuerzo', '/images/categories/lunch.jpg'),
('dinner', 'Dinner', 'Cena', '/images/categories/dinner.jpg'),
('dessert', 'Dessert', 'Postre', '/images/categories/dessert.jpg'),
('snack', 'Snack', 'Antojo', '/images/categories/snack.jpg'),
('drink', 'Drinks', 'Bebidas', '/images/categories/drink.jpg');

-- =====================================================
-- RECIPE 1: BANDEJA PAISA (Hard - Lunch)
-- =====================================================
INSERT INTO recipes (id, name, name_es, category, region, difficulty, prep_time_minutes, cook_time_minutes, servings, description, description_es, image_url) VALUES
('bandeja-paisa', 'Bandeja Paisa', 'Bandeja Paisa', 'lunch', 'Antioquia', 'hard', 30, 120, 4,
'Bandeja Paisa is Colombia''s most iconic dish, a hearty platter from the Antioquia region featuring red beans, rice, ground beef, chicharrón, fried egg, plantain, chorizo, arepa, and avocado.',
'La Bandeja Paisa es el plato más emblemático de Colombia, un abundante plato de la región de Antioquia con frijoles rojos, arroz, carne molida, chicharrón, huevo frito, plátano, chorizo, arepa y aguacate.',
'/images/recipes/bandeja-paisa.jpg');

INSERT INTO ingredients (recipe_id, name, name_es, amount, unit, order_index) VALUES
('bandeja-paisa', 'Red beans (dried)', 'Frijoles rojos', 500, 'g', 1),
('bandeja-paisa', 'Ground beef', 'Carne molida', 400, 'g', 2),
('bandeja-paisa', 'Chicharrón (pork belly)', 'Chicharrón', 200, 'g', 3),
('bandeja-paisa', 'White rice', 'Arroz blanco', 2, 'cups', 4),
('bandeja-paisa', 'Eggs', 'Huevos', 4, 'pieces', 5),
('bandeja-paisa', 'Ripe plantain', 'Plátano maduro', 2, 'pieces', 6),
('bandeja-paisa', 'Colombian chorizo', 'Chorizo', 4, 'pieces', 7),
('bandeja-paisa', 'Avocado', 'Aguacate', 1, 'piece', 8),
('bandeja-paisa', 'Arepas', 'Arepas', 4, 'pieces', 9),
('bandeja-paisa', 'Hogao sauce', 'Hogao', 1, 'cup', 10);

INSERT INTO steps (recipe_id, step_number, instruction, instruction_es) VALUES
('bandeja-paisa', 1, 'Soak beans overnight. Cook for 2 hours until tender, adding hogao in the last 30 minutes.', 'Remoje los frijoles durante la noche. Cocine por 2 horas hasta que estén tiernos, agregando hogao en los últimos 30 minutos.'),
('bandeja-paisa', 2, 'Season ground beef with salt, pepper, cumin, and garlic. Cook until browned.', 'Sazone la carne molida con sal, pimienta, comino y ajo. Cocine hasta dorar.'),
('bandeja-paisa', 3, 'Fry chicharrón until crispy and golden, about 5-7 minutes.', 'Fría el chicharrón hasta que esté crujiente y dorado, unos 5-7 minutos.'),
('bandeja-paisa', 4, 'Cook white rice according to package instructions.', 'Cocine el arroz según las instrucciones del paquete.'),
('bandeja-paisa', 5, 'Fry eggs sunny-side up, keeping yolks runny.', 'Fría los huevos con la yema hacia arriba.'),
('bandeja-paisa', 6, 'Slice plantains lengthwise and fry until golden on both sides.', 'Corte los plátanos a lo largo y fría hasta dorar por ambos lados.'),
('bandeja-paisa', 7, 'Grill chorizo until cooked through, about 8-10 minutes.', 'Ase el chorizo hasta que esté cocido, unos 8-10 minutos.'),
('bandeja-paisa', 8, 'Warm arepas on a dry skillet until lightly toasted.', 'Caliente las arepas en una sartén seca hasta tostar.'),
('bandeja-paisa', 9, 'Arrange all components on a large platter with sliced avocado. Serve immediately.', 'Organice todos los componentes en un plato grande con aguacate. Sirva inmediatamente.');

-- =====================================================
-- RECIPE 2: AJIACO (Medium - Lunch)
-- =====================================================
INSERT INTO recipes (id, name, name_es, category, region, difficulty, prep_time_minutes, cook_time_minutes, servings, description, description_es, image_url) VALUES
('ajiaco', 'Ajiaco Bogotano', 'Ajiaco Bogotano', 'lunch', 'Cundinamarca', 'medium', 20, 90, 6,
'Ajiaco is a traditional chicken and potato soup from Bogotá made with three types of potatoes and the aromatic herb guascas. Served with capers, cream, and avocado.',
'El Ajiaco es una sopa tradicional de pollo y papa de Bogotá, hecha con tres tipos de papas y la hierba aromática guascas. Se sirve con alcaparras, crema y aguacate.',
'/images/recipes/ajiaco.jpg');

INSERT INTO ingredients (recipe_id, name, name_es, amount, unit, order_index) VALUES
('ajiaco', 'Chicken pieces', 'Presas de pollo', 1, 'kg', 1),
('ajiaco', 'Papa criolla (yellow potatoes)', 'Papa criolla', 500, 'g', 2),
('ajiaco', 'Papa pastusa (white potatoes)', 'Papa pastusa', 500, 'g', 3),
('ajiaco', 'Papa sabanera (red potatoes)', 'Papa sabanera', 500, 'g', 4),
('ajiaco', 'Corn on the cob', 'Mazorcas', 3, 'pieces', 5),
('ajiaco', 'Guascas (dried herb)', 'Guascas', 3, 'tbsp', 6),
('ajiaco', 'Chicken broth', 'Caldo de pollo', 2, 'liters', 7),
('ajiaco', 'Green onions', 'Cebolla larga', 4, 'stalks', 8),
('ajiaco', 'Garlic cloves', 'Ajo', 4, 'pieces', 9),
('ajiaco', 'Capers', 'Alcaparras', 0.5, 'cup', 10),
('ajiaco', 'Heavy cream', 'Crema de leche', 1, 'cup', 11),
('ajiaco', 'Avocado', 'Aguacate', 2, 'pieces', 12);

INSERT INTO steps (recipe_id, step_number, instruction, instruction_es) VALUES
('ajiaco', 1, 'Simmer chicken in broth with green onions and garlic for 30 minutes.', 'Cocine el pollo en caldo con cebolla y ajo por 30 minutos.'),
('ajiaco', 2, 'Remove chicken and set aside. Keep broth simmering.', 'Retire el pollo y reserve. Mantenga el caldo a fuego lento.'),
('ajiaco', 3, 'Peel potatoes. Cube pastusa and sabanera, leave criolla whole.', 'Pele las papas. Corte pastusa y sabanera en cubos, deje criolla entera.'),
('ajiaco', 4, 'Add potatoes and corn to broth. Cook 45 minutes until criollas dissolve.', 'Agregue papas y maíz al caldo. Cocine 45 minutos hasta que las criollas se disuelvan.'),
('ajiaco', 5, 'Shred chicken, discarding bones and skin.', 'Deshebra el pollo, descartando huesos y piel.'),
('ajiaco', 6, 'Add guascas and cook 10 more minutes.', 'Agregue las guascas y cocine 10 minutos más.'),
('ajiaco', 7, 'Return chicken to pot. Season with salt.', 'Regrese el pollo a la olla. Sazone con sal.'),
('ajiaco', 8, 'Serve with capers, cream, and avocado on the side.', 'Sirva con alcaparras, crema y aguacate al lado.');

-- =====================================================
-- RECIPE 3: AREPAS (Easy - Breakfast)
-- =====================================================
INSERT INTO recipes (id, name, name_es, category, region, difficulty, prep_time_minutes, cook_time_minutes, servings, description, description_es, image_url) VALUES
('arepas', 'Colombian Arepas', 'Arepas Colombianas', 'breakfast', 'Nacional', 'easy', 10, 15, 8,
'Arepas are flatbreads made from ground maize dough, a staple of Colombian cuisine. These versatile corn cakes can be grilled, baked, or fried, and served with butter, cheese, or hogao.',
'Las arepas son panes planos de masa de maíz, un elemento básico de la cocina colombiana. Se pueden asar, hornear o freír, y servir con mantequilla, queso o hogao.',
'/images/recipes/arepas.jpg');

INSERT INTO ingredients (recipe_id, name, name_es, amount, unit, order_index) VALUES
('arepas', 'Pre-cooked corn flour (masarepa)', 'Harina de maíz precocida', 2, 'cups', 1),
('arepas', 'Warm water', 'Agua tibia', 2.5, 'cups', 2),
('arepas', 'Salt', 'Sal', 1, 'tsp', 3),
('arepas', 'Butter (softened)', 'Mantequilla', 2, 'tbsp', 4),
('arepas', 'Mozzarella cheese (optional)', 'Queso mozzarella (opcional)', 200, 'g', 5);

INSERT INTO steps (recipe_id, step_number, instruction, instruction_es) VALUES
('arepas', 1, 'Combine corn flour with salt in a bowl. Make a well in center.', 'Combine la harina con sal en un tazón. Haga un hueco en el centro.'),
('arepas', 2, 'Add warm water gradually, then butter. Knead until smooth. Rest 5 minutes.', 'Agregue agua tibia gradualmente, luego mantequilla. Amase hasta suavizar. Repose 5 minutos.'),
('arepas', 3, 'Divide into 8 portions. Form balls, then flatten into 3-inch discs.', 'Divida en 8 porciones. Forme bolas, luego aplane en discos de 8cm.'),
('arepas', 4, 'For cheese arepas: place cheese in center, fold dough around, reshape.', 'Para arepas de queso: coloque queso en el centro, doble la masa alrededor.'),
('arepas', 5, 'Cook on medium griddle 5-6 minutes per side until golden.', 'Cocine en plancha a fuego medio 5-6 minutos por lado hasta dorar.'),
('arepas', 6, 'Optional: finish in 350°F oven for 10 minutes for extra crispy.', 'Opcional: termine en horno a 180°C por 10 minutos para más crujientes.'),
('arepas', 7, 'Serve hot with butter, cheese, or hogao sauce.', 'Sirva caliente con mantequilla, queso o hogao.');
