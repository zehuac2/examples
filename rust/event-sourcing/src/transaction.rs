pub struct Transaction {
    pub id: usize,
    pub amount: f32,
}

impl Transaction {
    pub fn new(id: usize, amount: f32) -> Self {
        Transaction { id, amount }
    }
}
